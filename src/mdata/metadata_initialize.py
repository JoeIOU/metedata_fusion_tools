# ####metadata_initialize.py
# 元数据维护，包括entity，fields，relation等,从table、column的元数据来生成默认的entity和fields。
from config.config import cfg as config
from db.db_conn import db_connection_metedata as db_md
from mdata import metadata as md
from privilege import user_mngt as ur

logger = config.logger
# 数据表映射关系表名和字段元数据表名
MD_TABLES_NAME = "md_tables"
MD_COLUMNS_NAME = "md_columns"
# 数据表映射关系表名和字段元数据表名
MD_ENTITY_NAME = "md_entities"
MD_FIELDS_NAME = "md_fields"
MD_ENTITY_ID = "md_entity_id"
MD_ENTITY_REL_NAME = "md_entities_rel"

SQL_QUERY_ENTITY_FORMAT = """
            SELECT DISTINCT
                e.md_entity_id,
                e.md_entity_code,
                e.md_entity_name,
                f.md_fields_id,
                f.md_fields_name,
                tt.schema_code,
                tt.database_id,
                tt.md_tables_id,
                tt.md_tables_name,
                tt.md_tables_desc,
                cc.md_columns_id,
                cc.md_columns_name
            FROM
                md_entities e
            INNER JOIN md_tables tt ON e.md_tables_id = tt.md_tables_id
            INNER JOIN md_columns cc ON cc.md_tables_id = tt.md_tables_id
            INNER JOIN md_fields f ON f.md_entity_id = e.md_entity_id
            AND f.tenant_id = e.tenant_id
            AND f.md_columns_id = cc.md_columns_id
            WHERE
                e.tenant_id = %s
            AND tt.md_tables_name in %s
            """

SQL_QUERY_ENTITY_REL_FORMAT = """
            SELECT DISTINCT r.md_entity_rel_id,
                e.md_entity_id frm_md_entity_id,
                e.md_entity_code frm_md_entity_code,
                e.md_entity_name frm_md_entity_name,
                f.md_fields_id frm_md_fields_id,
                f.md_fields_name  frm_md_fields_name,
                e1.md_entity_id to_md_entity_id,
                e1.md_entity_code to_md_entity_code,
                e1.md_entity_name to_md_entity_name,
                f1.md_fields_id to_md_fields_id,
                f1.md_fields_name  to_md_fields_name
            FROM md_entities_rel r
            INNER JOIN  md_entities e on e.md_entity_id=r.from_entity_id
            INNER JOIN md_fields f ON f.md_entity_id = e.md_entity_id
            AND f.tenant_id = e.tenant_id and f.md_fields_id=r.from_field_id
            INNER JOIN  md_entities e1 on e1.md_entity_id=r.to_entity_id
            INNER JOIN md_fields f1 ON f1.md_entity_id = e1.md_entity_id
            AND f1.tenant_id = e1.tenant_id and f1.md_fields_id=r.to_field_id
            WHERE
                e.tenant_id = %s
               AND (e.md_entity_code in %s or e1.md_entity_code in %s)
             """


# 查询实体关系信息
def query_entity_rel_by_entity(tenant_id, entity_codes):
    sql = SQL_QUERY_ENTITY_REL_FORMAT
    if entity_codes is None:
        logger.warning("query_entity_rel_by_entity,entity_names should not be None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=(tenant_id, entity_codes, entity_codes))
    result = cursor.fetchall()
    return result

def query_entity_by_tenant(tenant_id, table_names):
    sql = SQL_QUERY_ENTITY_FORMAT
    if table_names is None:
        logger.warning("query_all_entity_in_schema,table_names should not be None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=(tenant_id, table_names))
    result = cursor.fetchall()
    return result


def initialize_md_entities_from_tables(user_id, tenant_id, entity_list):
    re = None
    if entity_list is None or len(entity_list) <= 0:
        return None
    md_table_ids = []
    table_name_list = []
    entity_code_list = []
    try:
        for tabl in entity_list:
            entity_code = tabl.get("entity_code")
            table_name = tabl.get("table_name")
            entity_code_list.append(entity_code)
            table_name_list.append(table_name)

        tables = md.get_md_tables_by_name(tenant_id, table_name_list)
        for item in tables:
            record = item.get("md_tables_id")
            if md_table_ids.count(record) <= 0:
                md_table_ids.append(record)
        if tables is None:
            return None
        columns = md.get_md_columns_multi_table(tenant_id, md_table_ids)
        i = 0
        res_col = None
        for code_ent in entity_code_list:
            tab_name = table_name_list[i]
            i += 1
            for table in tables:
                tab_name1 = table.get("md_tables_name")
                if not (tab_name1 is not None and tab_name1 == tab_name):
                    continue
                md_tables_id = table.get("md_tables_id")
                cols_new = get_columns_by_tables_id(md_tables_id, columns)
                is_sys_flag = True
                if cols_new is not None and len(cols_new) > 0:
                    for cl in cols_new:
                        if cl is not None:
                            md_entity_id_new = cl.get("md_columns_name")
                            # 存在MD_ENTITY_ID字段的表就不是系统表，而是租户数据表
                            if MD_ENTITY_ID == md_entity_id_new:
                                is_sys_flag = False
                                break
                res = ini_entities(user_id, tenant_id, code_ent, table, is_sys_flag)
                if res is None:
                    logger.warning(
                        "initialize_md_entities_from_tables,insert entity nothing ,user_id={},table:{}".format(user_id,
                                                                                                               table))
                    continue
                ids = res.get("data").get("ids")
                entity_id = ids[0]
                res_col = ini_fields(user_id, tenant_id, entity_id, cols_new)

        return res_col
    except Exception as e:
        logger.error("initialize_md_entities_from_tables insert error,msg:{}".format(e))
        raise e


def get_columns_by_tables_id(table_id, columns):
    if columns is None or table_id is None:
        return None
    cols = []
    for col in columns:
        md_tables_id = col.get("md_tables_id")
        if md_tables_id == table_id:
            cols.append(col)
    return cols


def ini_entities(user_id, tenant_id, new_entity_code, table_dict, is_sys_flag):
    res = md.get_md_entities_id_by_code([MD_ENTITY_NAME])
    if res is None:
        logger.warning("ini_entities,entity is None ,name:{}".format(MD_ENTITY_NAME))
        return None
    md_entity_id = res[0].get("md_entity_id")
    entity_list = []
    table = table_dict
    entity_dict = {}
    name = table.get("md_tables_desc")
    code = table.get("md_tables_name")
    if name is None or len(name) <= 0:
        name = code
    if new_entity_code is not None and len(new_entity_code.strip()) > 0:
        code = new_entity_code.strip()
        name = code
    entity_dict["md_entity_name"] = name
    entity_dict["md_entity_code"] = code
    entity_dict["md_entity_name_en"] = code
    entity_dict["md_entity_desc"] = name
    entity_dict["tenant_id"] = tenant_id
    entity_dict["md_tables_id"] = table.get("md_tables_id")
    if is_sys_flag:
        entity_dict["sys_flag"] = "Y"
    else:
        entity_dict["sys_flag"] = "N"
    entity_list.append(entity_dict)
    re = md.insert_execute(user_id, tenant_id, md_entity_id, entity_list)
    return re


def ini_fields(user_id, tenant_id, obj_id, columns):
    res = md.get_md_entities_id_by_code([MD_FIELDS_NAME])
    if res is None:
        logger.warning("ini_fields,entity is None ,name:{}".format(MD_FIELDS_NAME))
        return None
    if columns is None:
        logger.warning("ini_fields,columns is None ")
        return None
    md_entity_id = res[0].get("md_entity_id")
    fields_list = []
    for col in columns:
        field_dict = {}
        field_dict["md_entity_id"] = obj_id
        field_dict["md_columns_id"] = col.get("md_columns_id")
        field_dict["md_fields_name"] = col.get("md_columns_name")
        field_dict["md_fields_name_en"] = col.get("md_columns_name")
        field_dict["md_fields_type"] = col.get("md_columns_type")
        field_dict["md_fields_length"] = col.get("md_columns_length")
        field_dict["md_decimals_length"] = col.get("md_dec_length")
        field_dict["is_null"] = col.get("is_cols_null")
        field_dict["md_fields_desc"] = col.get("md_columns_desc")
        field_dict["is_unique"] = "N"
        field_dict["is_indexed"] = "N"
        field_dict["tenant_id"] = col.get("tenant_id")
        fields_list.append(field_dict)
    re = md.insert_execute(user_id, tenant_id, md_entity_id, fields_list)
    return re


def insert_metadata_table(user_id, tenant_id, tables):
    # 数据表md_tables的元数据实体ID
    # entity_id = 30018
    rr = md.get_md_entities_by_code(tenant_id, [MD_TABLES_NAME])
    re = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
        if entity_id is not None:
            re = md.insert_execute(user_id, tenant_id, entity_id, tables)
    if re is None:
        logger.warning("insert_metadata_table,get_md_entities_by_code is Null,tables=[{}].".format(MD_TABLES_NAME))
    return re


def insert_metadata_columns(user_id, tenant_id, columns):
    # 数据字段表md_columns的元数据实体ID
    # entity_id = 30014
    rr = md.get_md_entities_by_code(tenant_id, [MD_COLUMNS_NAME])
    re = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
        if entity_id is not None:
            re = md.insert_execute(user_id, tenant_id, entity_id, columns)
    if re is None:
        logger.warning("insert_metadata_columns,get_md_entities_by_code is Null,columns=[{}].".format(MD_COLUMNS_NAME))
    return re


def insert_metadata_entities_rel(user_id, tenant_id, entities_rel):
    rr = md.get_md_entities_by_code(tenant_id, [MD_ENTITY_REL_NAME])
    re = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
        if entity_id is not None:
            re = md.insert_execute(user_id, tenant_id, entity_id, entities_rel)
    if re is None:
        logger.warning(
            "insert_metadata_entities_rel,get_md_entities_by_code is Null,rel_table=[{}].".format(MD_ENTITY_REL_NAME))
    return re


if __name__ == '__main__':
    # [{"entity_code":"table_name"}]
    entity_list = [{"entity_code": "Contract", "table_name": "data_t"}, {"entity_code": "BoQ", "table_name": "data_t"}]
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    # 从数据库反向工程，初始化表和字段元数据
    # re = initialize_md_entities_from_tables(user_id, tenant_id, entity_list)
    tables = ["t001"]
    # 查询指定租户的所有实体和对应主键。
    re = query_entity_by_tenant(tenant_id, tables)
    logger.info("query all tables ,re={}".format(re))
