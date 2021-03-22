# ######index_unique.py
# 唯一值或索引值逻辑处理，在insert或者update数据时，同时要处理对应的索引表或者唯一键索引表，尽量放到一个事务处理或线程处理。
from db.db_conn import db_connection_metedata as db_md
from mdata import metadata as md
from privilege import user_mngt as ur
from config.config import cfg as config

logger = config.logger

FIELD_TYPE_TEXT = "Text"
FIELD_TYPE_CHAR = "Char"
FIELD_TYPE_INT = "Int"
FIELD_TYPE_DECIMAL = "Decimal"
FIELD_TYPE_DATE = "Date"

MD_INDEX_ENTITY_MAPPING_NAME = "index_mapping_t"
MD_ENTITY_INDEX_TEXT = "index_text_t"
MD_ENTITY_INDEX_INT = "index_int_t"
MD_ENTITY_INDEX_DEC = "index_decimal_t"
MD_ENTITY_INDEX_DATE = "index_date_t"
# MD_UNIQUE_ENTITY_MAPPING_NAME = "unique_mapping_t"
MD_ENTITY_UNIQUE_TEXT = "unique_text_t"
MD_ENTITY_UNIQUE_INT = "unique_int_t"
MD_ENTITY_UNIQUE_DEC = "unique_decimal_t"
MD_ENTITY_UNIQUE_DATE = "unique_date_t"

# 保存索引值的字段
MD_ENTITY_INDEX_FIELD_TEXT = "text_value"
MD_ENTITY_INDEX_FIELD_INT = "int_value"
MD_ENTITY_INDEX_FIELD_DEC = "num_value"
MD_ENTITY_INDEX_FIELD_DATE = "date_value"
# 保存数据id，默认data_id
MD_ENTITY_INDEX_DATA_FIELD = "data_id"

SQL_QUERY_INDEX_FORMAT = """
           SELECT
                t.index_mapping_id,
                t.tenant_id,
                t.md_entity_id,
                t.md_fields_id,
                t.mapping_type,
                t.unique_flag,
                f.md_fields_name,
                f.md_columns_id
            FROM
                index_mapping_t AS t
            INNER JOIN md_fields AS f ON f.tenant_id = t.tenant_id
            AND f.active_flag = 'Y'
            AND f.md_fields_id = t.md_fields_id
            WHERE
                t.tenant_id = %s
            AND t.md_entity_id = %s
            """


def query_index_mapping(tenant_id, entity_id):
    conn = db_md()
    cursor = conn.cursor()
    sql = SQL_QUERY_INDEX_FORMAT
    cursor.execute(sql, args=(tenant_id, entity_id,))
    result = cursor.fetchall()
    logger.info("query_index_mapping,entity:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


def query_index_all_type_list(tenant_id):
    code_list = []
    code_list.append(MD_ENTITY_INDEX_TEXT)
    code_list.append(MD_ENTITY_INDEX_DEC)
    code_list.append(MD_ENTITY_INDEX_INT)
    code_list.append(MD_ENTITY_INDEX_DATE)
    code_list.append(MD_ENTITY_UNIQUE_TEXT)
    code_list.append(MD_ENTITY_UNIQUE_DEC)
    code_list.append(MD_ENTITY_UNIQUE_INT)
    code_list.append(MD_ENTITY_UNIQUE_DATE)
    index_list = md.get_md_entities_by_code(tenant_id, code_list)
    return index_list


def get_mapping_table_fields(mapping_type, unique_flag):
    mapping_code, value_field = None, None
    if mapping_type is not None and (
            mapping_type.upper() == FIELD_TYPE_TEXT.upper() or mapping_type.upper() == FIELD_TYPE_CHAR.upper()):
        value_field = MD_ENTITY_INDEX_FIELD_TEXT
        if unique_flag is not None and unique_flag == "Y":
            mapping_code = MD_ENTITY_UNIQUE_TEXT
        else:
            mapping_code = MD_ENTITY_INDEX_TEXT
    elif mapping_type is not None and mapping_type.upper() == FIELD_TYPE_INT.upper():
        value_field = MD_ENTITY_INDEX_FIELD_INT
        if unique_flag is not None and unique_flag == "Y":
            mapping_code = MD_ENTITY_UNIQUE_INT
        else:
            mapping_code = MD_ENTITY_INDEX_INT
    elif mapping_type is not None and mapping_type.upper() == FIELD_TYPE_DECIMAL.upper():
        value_field = MD_ENTITY_INDEX_FIELD_DEC
        if unique_flag is not None and unique_flag == "Y":
            mapping_code = MD_ENTITY_UNIQUE_DEC
        else:
            mapping_code = MD_ENTITY_INDEX_DEC
    elif mapping_type is not None and mapping_type.upper() == FIELD_TYPE_DATE.upper():
        value_field = MD_ENTITY_INDEX_FIELD_DATE
        if unique_flag is not None and unique_flag == "Y":
            mapping_code = MD_ENTITY_UNIQUE_DATE
        else:
            mapping_code = MD_ENTITY_INDEX_DATE
    return mapping_code, value_field


def gen_index_mapping(tenant_id, data_list):
    index_list = query_index_all_type_list(tenant_id)
    classify_dict = {}
    for item in data_list:
        unique_flag = item.get("unique_flag")
        mapping_type = item.get("mapping_type")
        # 删除非元数据存储字段信息，避免影响保存动作
        item.pop("mapping_type")
        item.pop("unique_flag")
        if unique_flag == "Y":
            mapping_code, value_field = get_mapping_table_fields(mapping_type, unique_flag)
            for itm in index_list:
                code = itm.get("md_entity_code")
                if code == mapping_code:
                    entity_id = itm.get("md_entity_id")
                    obj_list = classify_dict.get(str(entity_id))
                    if obj_list is None:
                        tmp_li = []
                        tmp_li.append(item)
                        classify_dict[str(entity_id)] = tmp_li
                    else:
                        obj_list.append(item)
                    break
        # 不管索引，还是唯一索引，都在index对应的表有存记录。
        mapping_code, value_field = get_mapping_table_fields(mapping_type, "N")
        for itm in index_list:
            code = itm.get("md_entity_code")
            if code == mapping_code:
                entity_id = itm.get("md_entity_id")
                obj_list = classify_dict.get(str(entity_id))
                if obj_list is None:
                    tmp_li = []
                    tmp_li.append(item)
                    classify_dict[str(entity_id)] = tmp_li
                else:
                    obj_list.append(item)
                break
    return classify_dict


def exec_index_action(user_id, tenant_id, new_data_list, delete_only=False):
    classify_dict = gen_index_mapping(tenant_id, new_data_list)
    re = None
    for key in classify_dict.keys():
        if key is not None:
            entity_id1 = int(key)
            ls_tmp = classify_dict.get(key)
            ls_del = get_delete_list(ls_tmp)
            re = md.delete_execute(user_id, tenant_id, entity_id1, ls_del)
            if not delete_only:
                re = md.insert_execute(user_id, tenant_id, entity_id1, ls_tmp)
    return re


def get_delete_list(del_list):
    if del_list is None:
        return None
    list_res = []
    for item in del_list:
        itm = {}
        data_id = item.get(MD_ENTITY_INDEX_DATA_FIELD)
        if data_id is None:
            continue
        itm[MD_ENTITY_INDEX_DATA_FIELD] = data_id
        itm["md_entity_id"] = item.get("md_entity_id")
        itm["md_fields_id"] = item.get("md_fields_id")
        list_res.append(itm)
    return list_res


def get_mapping_list(data_list, mapping_list, ids):
    data_list_new = []
    if data_list is None or len(data_list) <= 0:
        return None
    if mapping_list is not None and len(mapping_list) >= 0:
        for item in mapping_list:
            mapping_entity_id = item.get("md_entity_id")
            mapping_field_id = item.get("md_fields_id")
            mapping_field_name = item.get("md_fields_name")
            unique_flag = item.get("unique_flag")
            mapping_type = item.get("mapping_type")
            mapping_code, value_field = get_mapping_table_fields(mapping_type, unique_flag)
            i = 0
            for itm in data_list:
                id = ids[i]
                i += 1
                entity_id = itm.get("md_entity_id")
                i_entity_id = -1
                if isinstance(entity_id, str):
                    i_entity_id = int(entity_id)
                else:
                    i_entity_id = entity_id
                # field_id = itm.get("md_fields_id")
                if mapping_field_name is not None and mapping_field_name in itm.keys() and mapping_entity_id == i_entity_id:
                    item_new = {}
                    item_new["md_entity_id"] = mapping_entity_id
                    item_new["unique_flag"] = unique_flag
                    item_new["mapping_type"] = mapping_type
                    item_new["md_fields_id"] = mapping_field_id
                    item_new[value_field] = itm.get(mapping_field_name)
                    item_new[MD_ENTITY_INDEX_DATA_FIELD] = id
                    data_list_new.append(item_new)
    return data_list_new


def get_mapping_del_list(md_entity_id, mapping_list, ids):
    data_list_new = []
    if mapping_list is not None and len(mapping_list) >= 0:
        for item in mapping_list:
            mapping_entity_id = item.get("md_entity_id")
            mapping_field_id = item.get("md_fields_id")
            # mapping_field_name = item.get("md_fields_name")
            unique_flag = item.get("unique_flag")
            mapping_type = item.get("mapping_type")
            # mapping_code, value_field = get_mapping_table_fields(mapping_type, unique_flag)
            i = 0
            i_entity_id = -1
            if isinstance(md_entity_id, str):
                i_entity_id = int(md_entity_id)
            else:
                i_entity_id = md_entity_id
            for id in ids:
                if mapping_entity_id == i_entity_id:
                    item_new = {}
                    item_new["md_entity_id"] = mapping_entity_id
                    item_new["unique_flag"] = unique_flag
                    item_new["mapping_type"] = mapping_type
                    item_new["md_fields_id"] = mapping_field_id
                    # item_new[value_field] = itm.get(mapping_field_name)
                    item_new[MD_ENTITY_INDEX_DATA_FIELD] = id
                    data_list_new.append(item_new)
    return data_list_new


def insert_index_data(user_id, tenant_id, md_entity_id, data_list, ids):
    re = None
    if ids is None:
        logger.warning(
            "insert_index_data,insert ids is None,entity_id=[{}],data:{}.".format(md_entity_id, data_list))
        return None

    if md_entity_id is not None:
        mapping_list = query_index_mapping(tenant_id, md_entity_id)
        new_list = get_mapping_list(data_list, mapping_list, ids)
        if new_list is not None:
            re = exec_index_action(user_id, tenant_id, new_list)
    if re is None:
        logger.warning(
            "insert_index_data,insert nothing,entity_id=[{}],data:{}.".format(md_entity_id, data_list))
    return re


def update_index_data(user_id, tenant_id, md_entity_id, data_list, ids):
    re = None
    new_list = None
    if md_entity_id is not None:
        mapping_list = query_index_mapping(tenant_id, md_entity_id)
        new_list = get_mapping_list(data_list, mapping_list, ids)
        if new_list is not None and len(new_list) > 0:
            re = exec_index_action(user_id, tenant_id, new_list)
    if new_list is not None and len(new_list) > 0 and re is None:
        logger.warning(
            "update_index_data,update nothing,entity_id=[{}],data:{}.".format(md_entity_id, data_list))
    return re


def delete_index_data(user_id, tenant_id, md_entity_id, data_list, ids):
    re, new_list = None, None
    if md_entity_id is not None:
        mapping_list = query_index_mapping(tenant_id, md_entity_id)
        new_list = get_mapping_del_list(md_entity_id, mapping_list, ids)
        if new_list is not None:
            re = exec_index_action(user_id, tenant_id, new_list, delete_only=True)
    if re is None:
        logger.warning(
            "delete_index_data,delete nothing,entity_id=[{}],data:{}.".format(md_entity_id, new_list))
    return re


if __name__ == '__main__':
    # ##insert the index data
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    # data_list = []
    datas = [{
        'test_fields': 'kiki-001',
        'test_fields1': 'kiki',
        'customer_name': "ABC.com",
        "md_entity_id": 30001
    }, {
        'test_fields': 'goog-001',
        'test_fields1': 'gogo',
        'customer_name': "HW.com",
        "md_entity_id": 30001
    }]
    md_entity_id = 30001

    re = query_index_mapping(tenant_id, md_entity_id)
    print(re)
    ids = [12421421412, 12421421411]
    re = insert_index_data(user_id, tenant_id, md_entity_id, datas, ids)
    # re = update_index_data(user_id, tenant_id, md_entity_id, datas, ids)
    # re = delete_index_data(user_id, tenant_id, md_entity_id, datas, ids)
