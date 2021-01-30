##metadata_eng_reverse.py
# 数据库反向工程，写入元数据表和字段，以及建立实体外键关系等。
from config.config import cfg as config
from mdata import metadata_initialize as mdi
from mdata import user_mngt as ur

logger = config.logger


# 从数据库表约束关系，反向工程生成，初始化元数据实体
def intialize_entity_rel_from_schema(user_id, tenant_id, schema, const_list):
    if schema is None:
        logger.info("intialize_entity_rel_from_schema,schema should not be NULL.")
        return None
    if const_list is None:
        logger.info("intialize_entity_rel_from_schema,constraint should not be NULL.")
        return None
    t_list = get_tables_from_constraint(const_list)
    result_list = []
    if t_list is not None and len(t_list) > 0:
        iCount = len(t_list)
        size = 100
        i = 0
        while True:
            i += 1
            i_from = (i - 1) * size
            i_to = i * size
            if i_from >= iCount:
                break
            if i_to > iCount:
                i_to = iCount
            list_split = t_list[i_from:i_to]
            entity_res = mdi.query_entity_by_tenant(tenant_id, list_split)
            entities_rel = combine_constraint_rel(const_list, entity_res)
            result = mdi.insert_metadata_entities_rel(user_id, tenant_id, entities_rel)
            result_list.append(result)
    return result_list


def get_tables_from_constraint(const_list):
    if const_list is None:
        return None
    ls_tables = []
    for item in const_list:
        table_name = item.get("TABLE_NAME")
        table_name_ref = item.get("REFERENCED_TABLE_NAME")
        if table_name is not None and ls_tables.count(table_name) <= 0:
            ls_tables.append(table_name)
        if table_name_ref is not None and ls_tables.count(table_name_ref) <= 0:
            ls_tables.append(table_name_ref)
    return ls_tables


def combine_constraint_rel(table_constraint_list, entity_list):
    if table_constraint_list is None:
        return None
    if entity_list is None:
        logger.info("combine_constraint_rel,entity_list should not be NULL.")
        return None
    ent_list = []
    for item in table_constraint_list:
        # constraint_name = item.get("CONSTRAINT_NAME")
        schema = item.get("TABLE_SCHEMA")
        schema_ref = item.get("REFERENCED_TABLE_SCHEMA")
        table_name = item.get("TABLE_NAME")
        col_name = item.get("COLUMN_NAME")
        table_name_ref = item.get("REFERENCED_TABLE_NAME")
        col_name_ref = item.get("REFERENCED_COLUMN_NAME")
        entity_dict, entity_dict1 = None, None
        for itm in entity_list:
            schema_code = itm.get("schema_code")
            md_tables_name = itm.get("md_tables_name")
            md_columns_name = itm.get("md_columns_name")
            # md_entity_name = itm.get("md_entity_name")
            if schema is not None and schema_code is not None and schema.upper() == schema_code.upper() \
                    and table_name is not None and md_tables_name is not None and table_name.upper() == md_tables_name.upper() \
                    and col_name is not None and md_columns_name is not None and col_name.upper() == md_columns_name.upper():
                entity_dict = itm
                break
        for itm1 in entity_list:
            schema_code = itm1.get("schema_code")
            md_tables_name = itm1.get("md_tables_name")
            md_columns_name = itm1.get("md_columns_name")
            # md_entity_name = itm1.get("md_entity_name")
            if schema_ref is not None and schema_code is not None and schema_ref.upper() == schema_code.upper() \
                    and table_name_ref is not None and md_tables_name is not None and table_name_ref.upper() == md_tables_name.upper() \
                    and col_name_ref is not None and md_columns_name is not None and col_name_ref.upper() == md_columns_name.upper():
                md_entity_id = itm1.get("md_entity_id")
                md_fields_id = itm1.get("md_fields_id")
                md_entity_name = itm1.get("md_entity_name")
                if entity_dict is not None:
                    entity_dict1 = {}
                    entity_dict1["rel_type"] = "1:N"
                    entity_dict1["to_entity_id"] = entity_dict.get("md_entity_id")
                    entity_dict1["to_field_id"] = entity_dict.get("md_fields_id")
                    entity_dict1["from_entity_id"] = md_entity_id
                    entity_dict1["from_field_id"] = md_fields_id
                    rel_name = entity_dict.get("md_entity_name") + " AND " + md_entity_name + " RELATION"
                    entity_dict1["md_entity_rel_desc"] = rel_name
                    entity_dict1["active_flag"] = "Y"
                    ent_list.append(entity_dict1)
                break

    return ent_list


# 从数据库表和字段信息，反向工程生成，初始化表和字段元数据
def intialize_md_tables_from_schema(user_id, tenant_id, database_name, schema, tables_list, columns_list):
    if tables_list is None or len(tables_list) == 0:
        logger.info("get_table_column_info,tables input param should not be NULL.")
        return None
    logger.info("get_table_column_info,tables_info:{}.".format(tables_list))
    tables = []
    for item in tables_list:
        row = {}
        table_name = item.get("TABLE_NAME")
        table_desc = item.get("TABLE_COMMENT")
        if table_desc is None or len(table_desc) <= 0:
            table_desc = table_name
        row["md_tables_name"] = table_name
        row["md_tables_desc"] = table_desc
        row["database_id"] = database_name
        row["schema_code"] = schema
        tables.append(row)
    logger.info("get_table_column_info,re={}".format(columns_list))
    columns=[]
    for item in columns_list:
        column = {}
        table_name = item.get("TABLE_NAME")
        column["md_columns_name"] = item.get("COLUMN_NAME")
        column["md_columns_type"] = item.get("DATA_TYPE")
        column["md_columns_length"] = item.get("NUMERIC_PRECISION")
        column["md_dec_length"] = item.get("NUMERIC_SCALE")
        key = item.get("COLUMN_KEY")
        is_key = "N"
        if key is not None and key == "PRI":
            is_key = "Y"
        column["is_key"] = is_key
        column["md_columns_desc"] = item.get("COLUMN_COMMENT")
        # column[""] = item.get("COLUMN_TYPE")
        is_null = item.get("IS_NULLABLE")
        is_null_flag = "Y"
        if is_null is not None and (is_null == "NO" or is_null == "N" ):
            is_null_flag = "N"
        column["is_cols_null"] = is_null_flag
        column["md_tables_id"] = table_name
        columns.append(column)

    for item in tables:
        table_name_new = item.get("md_tables_name")
        if table_name_new is None:
            continue
        re = mdi.insert_metadata_table(user_id, tenant_id, [item])
        if re is None:
            continue
        ids = re.get("data").get("ids")
        id = None
        if ids is not None and len(ids) >= 0:
            id = ids[0]
        logger.info("insert_metadata_table,re={}".format(re))
        columns_new = []
        for col in columns:
            if col.get("md_tables_id") == table_name_new:
                col["md_tables_id"] = id
                columns_new.append(col)
        re = mdi.insert_metadata_columns(user_id, tenant_id, columns_new)
        logger.info("insert_metadata_columns,re={}".format(re))
    return tables


if __name__ == '__main__':
    # ##insert the metadata of table and columns into meatadata tables
    tables_list = ['t001']
    schema = "test"
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    database_name = "MySql"
    ##1.初始化实体和字段信息，反向从数据库
    # intialize_md_tables_from_schema(user_id, tenant_id, database_name, schema, tables_list)
    table_consts = None  # ["data_lookup_set"] ,为None则处理当前Schema下的所有关系。
    ##1.初始化实体关系，反向从数据库的外键关系
    re = intialize_entity_rel_from_schema(user_id, tenant_id, schema, table_consts)

    # ####get all tables in the schema
    schema = "test"
    # re = get_all_table_in_the_schema(schema)
    logger.info("all tables in[{}],re={}".format(schema, re))
