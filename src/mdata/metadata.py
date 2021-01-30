# ####metadata.py
import time, datetime
import decimal
from common.guid import get_guid
from db.db_conn import db_connection_metedata as db_md
from config.config import cfg as config
from privilege import data_privilege as dp, user_mngt as ur
from common import constants as const

logger = config.logger
# 执行sql操作类型CRUD等
DB_EXEC_TYPE_INSERT = "INSERT"
DB_EXEC_TYPE_UPDATE = "UPDATE"
DB_EXEC_TYPE_DELETE = "DELETE"
DB_EXEC_TYPE_QUERY = "QUERY"
# 执行sql的返回状态
DB_EXEC_STATUS_SUCCESS = 200
DB_EXEC_STATUS_FAIL = 500
DB_EXEC_STATUS_PANDING = 100
DB_EXEC_STATUS_OVERTIME = 501

KEY_FIELDS_ID = "__obj_id__"


# 元数据实体
def get_md_entities(tenant_id, md_entity_ids):
    if md_entity_ids is None or len(md_entity_ids) <= 0:
        logger.warning("get_md_entities,md_entity_ids is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_id in %s"
    cursor.execute(sql, args=(tenant_id, md_entity_ids,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("get_md_entities,entitire:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据实体通过实体code编码
def get_md_entities_by_code(tenant_id, md_entity_codes):
    if md_entity_codes is None or len(md_entity_codes) <= 0:
        logger.warning("get_md_entities_by_name,md_entity_names is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_code in %s"
    cursor.execute(sql, args=(tenant_id, md_entity_codes,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_entities:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据实体通过实体code编码查找ID
def get_md_entities_id_by_code(md_entity_codes):
    if md_entity_codes is None or len(md_entity_codes) <= 0:
        logger.warning("get_md_entities_by_name,md_entity_names is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select md_entity_id,md_entity_code,md_tables_id from md_entities where active_flag='Y' and md_entity_code in %s"
    cursor.execute(sql, args=(md_entity_codes,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_entitire_ids:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据实体通过实体名称
def get_md_entities_by_name(tenant_id, md_entity_names):
    if md_entity_names is None or len(md_entity_names) <= 0:
        logger.warning("get_md_entities_by_name,md_entity_names is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_name in %s"
    cursor.execute(sql, args=(tenant_id, md_entity_names,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_entitire:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据属性
def get_md_fields(tenant_id, md_entity_id):
    if md_entity_id is None:
        logger.warning("get_md_fields,md_entity_id is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_fields where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_id=%s"
    cursor.execute(sql, args=(tenant_id, md_entity_id,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_fields:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 多个实体元数据属性
def get_md_fields_multi_entity(tenant_id, md_entity_ids):
    if md_entity_ids is None:
        logger.warning("get_md_fields_multi_entity,md_entity_ids is None")
        return None
    ls = []
    for item in md_entity_ids:
        if item is not None:
            re = get_md_fields(tenant_id, item)
            ls.append(re)
    return ls


# 元数据DB表映射
def get_md_tables(tenant_id, md_table_ids):
    if md_table_ids is None or len(md_table_ids) == 0:
        logger.warning("get_md_tables,md_table_ids is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_tables where active_flag='Y'and (tenant_id=%s or public_flag='Y') and  md_tables_id in %s"
    cursor.execute(sql, args=(tenant_id, md_table_ids,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_tables:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据DB表映射通过表名
def get_md_tables_by_name(tenant_id, md_table_names):
    if md_table_names is None or len(md_table_names) == 0:
        logger.warning("get_md_tables_by_name,md_table_names is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_tables where active_flag='Y' and (tenant_id=%s or public_flag='Y')and  md_tables_name in %s"
    cursor.execute(sql, args=(tenant_id, md_table_names,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_tables by Name:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据数据表字段映射
def get_md_columns(tenant_id, md_table_id):
    if md_table_id is None:
        logger.warning("get_md_columns,md_table_id is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_columns where active_flag='Y' and (tenant_id=%s or public_flag='Y') and  md_tables_id =%s"
    cursor.execute(sql, args=(tenant_id, md_table_id,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_columns:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 多个表的属性字段信息
def get_md_columns_multi_table(tenant_id, md_table_ids):
    if md_table_ids is None:
        logger.warning("get_md_columns_multi_table,md_table_ids is None")
        return None
    ls = []
    for item in md_table_ids:
        if item is not None:
            re = get_md_columns(tenant_id, item)
            ls += re
    return ls


# 获取表名和所有字段信息
def get_table_all_columns(tenant_id, md_table_ids):
    if md_table_ids is None:
        logger.warning("get_table_all_columns,md_table_ids is None")
        return None
    table_list = get_md_tables(tenant_id, md_table_ids)
    column_list = get_md_columns_multi_table(tenant_id, md_table_ids)
    for col in column_list:
        for t in table_list:
            if t['md_tables_id'] == col.get('md_tables_id'):
                col['md_tables_name'] = t.get('md_tables_name')
                break
    # re = []
    return column_list


# 元数据数据表关键字字段映射
def get_md_key_columns(md_table_ids):
    if md_table_ids is None:
        logger.warning("get_md_key_columns,md_table_ids is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select * from md_columns where active_flag='Y' and is_key='Y' and  md_tables_id in %s)"
    cursor.execute(sql, args=(md_table_ids,))
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_columns:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 实体关系表
def get_md_entities_rel(tenant_id, from_entity_ids, to_entity_ids):
    if from_entity_ids is None and to_entity_ids is None:
        logger.warning("get_md_entities_rel,to_entity_ids and from_entity_ids is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    if (from_entity_ids is None or len(from_entity_ids) <= 0) and (to_entity_ids is None or len(to_entity_ids) <= 0):
        return None
    sql = "select distinct * from md_entities_rel where active_flag='Y' and tenant_id=%s "
    if (from_entity_ids is not None and len(from_entity_ids) > 0) and (
            to_entity_ids is not None and len(to_entity_ids) > 0):
        sql += "and (from_entity_id in %s and to_entity_id in %s)"
        arg = (tenant_id, from_entity_ids, to_entity_ids,)
    elif (from_entity_ids is not None and len(from_entity_ids) > 0):
        sql += "and (from_entity_id in %s)"
        arg = (tenant_id, from_entity_ids,)
    elif (to_entity_ids is not None and len(to_entity_ids) > 0):
        sql += "and (to_entity_id in %s)"
        arg = (tenant_id, to_entity_ids,)
    else:
        return None
    cursor.execute(sql, args=arg)
    result = cursor.fetchall()
    result = fetch_record2list(result)
    logger.info("md_entitire_rel:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 实体所有属性信息查询
def get_entity_all_fields(tenant_id, entity_ids, filter_fields=None):
    if entity_ids is None:
        logger.warning("get_entity_all_fields,entity_ids is None")
        return None
    entities = get_md_entities(tenant_id, entity_ids)
    tables_list = []
    entity_list = []
    tables = []
    fields = []
    columns = []
    for item in entities:
        tables_id = item.get('md_tables_id')
        md_entity_id = item.get('md_entity_id')
        if entity_list.count(md_entity_id) <= 0:
            entity_list.append(md_entity_id)
            fields += get_md_fields(tenant_id, md_entity_id)
        if tables_list.count(tables_id) > 0:
            continue
        else:
            tables_list.append(tables_id)
            columns += get_md_columns(tenant_id, tables_id)
    if tables_list is None or len(tables_list) == 0:
        logger.warning("get_entity_all_fields,tables_list is None")
        return None
    tables = get_md_tables(tenant_id, tables_list)
    re = combine_entity_all_fields(entities, fields, tables, columns, filter_fields)
    re.sort(key=lambda k: (k.get('md_entity_id', 0), k.get('md_fields_id', 0)))
    return re


# 实体+表对应关系信息查询
def get_entity_table_mapping(tenant_id, entity_ids):
    if entity_ids is None:
        logger.warning("get_entity_table_mapping,entity_ids is None")
        return None
    entities = get_md_entities(tenant_id, entity_ids)
    if entities is None or len(entities) <= 0:
        return None
    tables_list = []
    entity_list = []
    tables = []
    for item in entities:
        tables_id = item.get('md_tables_id')
        md_entity_id = item.get('md_entity_id')
        if entity_list.count(md_entity_id) <= 0:
            entity_list.append(md_entity_id)
        if tables_list.count(tables_id) > 0:
            continue
        else:
            tables_list.append(tables_id)
    tables = get_md_tables(tenant_id, tables_list)
    re = combine_entity_table(entities, tables)
    re.sort(key=lambda k: (k.get('md_entity_id', 0), k.get('md_tables_id', 0)))
    return re


# 实体和表对应关系组合
def combine_entity_table(entities, tables):
    if entities is None:
        logger.warning("combine_entity_table,entities is None")
        return None
    list = []
    for item in entities:
        entity = {}
        dict_new = {}
        entity_id = item.get('md_entity_id')
        entity['md_entity_id'] = entity_id
        entity['md_entity_name'] = item.get('md_entity_name')
        entity['md_entity_name_en'] = item.get('md_entity_name_en')
        entity['md_entity_desc'] = item.get('md_entity_desc')
        entity['tenant_id'] = item.get('tenant_id')
        table_id = item.get('md_tables_id')
        entity['md_tables_id'] = table_id
        dict_new = entity
        if tables is not None and len(tables) > 0:
            for table in tables:
                if table_id == table.get('md_tables_id'):
                    t = {}
                    t['md_tables_name'] = table.get('md_tables_name')
                    dict_new = dict(dict_new, **t)
                    list.append(dict_new)
                    break
        else:
            list.append(dict_new)

    logger.info("combine_entity_tables:{}".format(list))
    return list


# 实体属性和字段组合
def combine_entity_all_fields(entities, fields, tables, columns, filter_fields=None):
    if entities is None or len(entities) == 0:
        logger.warning("combine_entity_all_fields,entities is None")
        return None
    list = []
    for item in entities:
        entity = {}
        entity_id = item.get('md_entity_id')
        entity['md_entity_id'] = entity_id
        entity['md_entity_name'] = item.get('md_entity_name')
        entity['md_entity_name_en'] = item.get('md_entity_name_en')
        entity['md_entity_desc'] = item.get('md_entity_desc')
        entity['tenant_id'] = item.get('tenant_id')
        entity['sys_flag'] = item.get('sys_flag')
        table_id = item.get('md_tables_id')
        entity['md_tables_id'] = table_id
        # list.append(entity)
        for field in fields:
            if entity_id != field.get('md_entity_id'):
                continue
            ff = field.get('md_fields_id')
            if filter_fields is not None and len(filter_fields) > 0:
                flag = False
                for filter_field in filter_fields:
                    if ff == filter_field:
                        flag = True
                        break
                if not flag:
                    continue
            f = {}
            f['md_fields_id'] = ff
            f['md_fields_name'] = field.get('md_fields_name')
            f['md_fields_type'] = field.get('md_fields_type')
            column_id = field.get('md_columns_id')
            f['md_columns_id'] = column_id
            f['lookup_flag'] = field.get('lookup_flag')
            dict_new = dict(f, **entity)
            if tables is not None and len(tables) > 0:
                for table in tables:
                    if table_id == table.get('md_tables_id'):
                        t = {}
                        t['md_tables_name'] = table.get('md_tables_name')
                        dict_new = dict(dict_new, **t)
                        for column in columns:
                            if column_id == column.get('md_columns_id'):
                                c = {}
                                c['md_columns_name'] = column.get('md_columns_name')
                                c['md_columns_type'] = column.get('md_columns_type')
                                c['is_cols_null'] = column.get('is_cols_null')
                                c['md_columns_length'] = column.get('md_columns_length')
                                c['md_dec_length'] = column.get('md_dec_length')
                                c['is_key'] = column.get('is_key')
                                dict_new = dict(dict_new, **c)
                                list.append(dict_new)
            else:
                list.append(dict_new)

    logger.info("combine_entity_all_fields_columns:{}".format(list))
    return list
