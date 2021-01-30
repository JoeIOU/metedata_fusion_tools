# ####schema_mysql.py
# MySql数据库表反向工程，生成表和字段等元数据存入元数据表。
from config.config import cfg as config
from db.db_conn import db_connection_data as db
from schema import metadata_eng_reverse as mdr
from mdata import user_mngt as ur

logger = config.logger

schema_info_all_table_sql_format = """
                                SELECT distinct
                                    aa.TABLE_SCHEMA,
                                    aa.TABLE_NAME,
                                    cc.TABLE_COMMENT
                                FROM
                                    information_schema.`COLUMNS` aa
                                LEFT JOIN 
                                        information_schema.`TABLES` cc
                                  ON 
                                    aa.TABLE_SCHEMA = cc.TABLE_SCHEMA
                                    AND aa.TABLE_NAME = cc.TABLE_NAME
                                WHERE
                                    aa.TABLE_SCHEMA = %s     
                        """
schema_info_table_sql_format = schema_info_all_table_sql_format + " AND aa.TABLE_NAME in %s"

schema_info_column_sql_format = """
                                SELECT
                                    aa.TABLE_SCHEMA,
                                    aa.TABLE_NAME,
                                    aa.COLUMN_NAME,
                                    aa.DATA_TYPE,
                                    IFNULL(aa.CHARACTER_MAXIMUM_LENGTH,
                                    aa.NUMERIC_PRECISION) as NUMERIC_PRECISION,
                                    aa.NUMERIC_SCALE,
                                    aa.COLUMN_KEY,
                                    aa.COLUMN_COMMENT,
                                    aa.IS_NULLABLE
                                FROM
                                    information_schema.`COLUMNS` aa
                                WHERE
                                    aa.TABLE_SCHEMA = %s
                                AND aa.TABLE_NAME in %s
                        """

schema_all_table_constraint_sql_format = """
                                SELECT
                                    CONSTRAINT_CATALOG,
                                    CONSTRAINT_SCHEMA,
                                    CONSTRAINT_NAME,
                                    TABLE_CATALOG,
                                    TABLE_SCHEMA,
                                    TABLE_NAME,
                                    COLUMN_NAME,
                                    ORDINAL_POSITION,
                                    POSITION_IN_UNIQUE_CONSTRAINT,
                                    REFERENCED_TABLE_SCHEMA,
                                    REFERENCED_TABLE_NAME,
                                    REFERENCED_COLUMN_NAME
                                FROM
                                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE t
                                WHERE
                                    t.TABLE_SCHEMA = %s
                                AND t.REFERENCED_COLUMN_NAME IS NOT NULL
"""

special_table_constraint_sql_format = schema_all_table_constraint_sql_format + " AND t.TABLE_NAME in %s"


def get_all_table_in_the_schema(schema):
    if schema is None:
        logger.warning("get_table_info,schema should not be None")
        return None
    conn = db()
    cursor = conn.cursor()
    sql = schema_info_all_table_sql_format
    cursor.execute(sql, args=(schema))
    result = cursor.fetchall()
    return result


def get_table_info(schema, table_name_list):
    if schema is None:
        logger.warning("get_table_info,schema should not be None")
        return None
    if table_name_list is None:
        logger.warning("get_table_info,table_name should not be None")
        return None
    conn = db()
    cursor = conn.cursor()
    sql = schema_info_table_sql_format
    cursor.execute(sql, args=(schema, table_name_list))
    result = cursor.fetchall()
    return result


def get_table_column_info(schema, table_name_list):
    if schema is None:
        logger.warning("get_table_column_info,schema should not be None")
        return None
    if table_name_list is None:
        logger.warning("get_table_column_info,table_name should not be None")
        return None
    conn = db()
    cursor = conn.cursor()
    sql = schema_info_column_sql_format
    cursor.execute(sql, args=(schema, table_name_list))
    result = cursor.fetchall()
    return result


def get_constraint_info(schema, tables):
    if schema is None:
        logger.warning("get_constraint_info,schema should not be None")
        return None
    conn = db()
    cursor = conn.cursor()
    if tables is not None:
        sql = special_table_constraint_sql_format
        cursor.execute(sql, args=(schema, tables))
    else:
        sql = schema_all_table_constraint_sql_format
        cursor.execute(sql, args=(schema))
    result = cursor.fetchall()
    return result


##1.初始化表和字段信息，反向从数据库
def reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list):
    tables = get_table_info(schema, tables_list)
    columns = get_table_column_info(schema, tables_list)
    re = mdr.intialize_md_tables_from_schema(user_id, tenant_id, database_name, schema, tables, columns)
    return re


##2.初始化实体关系，反向从数据库的外键关系（前提：entity和fields等元数据已经生成）
def reverse_constraint(user_id, tenant_id, schema, tables_list):
    const_list = get_constraint_info(schema, tables_list)
    re = mdr.intialize_entity_rel_from_schema(user_id, tenant_id, schema, const_list)
    return re


if __name__ == '__main__':
    # ##insert the metadata of table and columns into meatadata tables
    schema = "test"
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    database_name = "MySql"
    tables_list = ['roles']
    re = reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list)
    logger.info("all tables in[{}],re={}".format(schema, re))

    # re = reverse_constraint(user_id, tenant_id, schema, tables_list)
    # logger.info("all tables in[{}],re={}".format(schema, re))

    # tables = None  # ["data_lookup_set"] ,为None则处理当前Schema下的所有关系。
    # ####get all tables in the schema
    # schema = "test"
    # re = get_all_table_in_the_schema(schema)
    # logger.info("all tables in[{}],re={}".format(schema, re))
