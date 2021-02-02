# ####schema_oracle.py
# Oracle数据库表反向工程，生成元数据存入表。
from config.config import cfg as config
from db.db_conn import db_connection_oracle as con_oracle
from schema import metadata_eng_reverse as mdr
from privilege import user_mngt as ur

logger = config.logger

schema_info_all_table_sql_format_oracle = """ 
             select c.OWNER as TABLE_SCHEMA,
                   c.TABLE_NAME,
                   nvl(cc.COMMENTS, c.TABLE_NAME) as TABLE_COMMENT
              from all_tables c, all_tab_comments cc
             where cc.TABLE_NAME = c.TABLE_NAME
               and c.OWNER = cc.OWNER
               and c.OWNER = :SCHEMA
            """
schema_info_table_sql_format_oracle = schema_info_all_table_sql_format_oracle + " and c.TABLE_NAME in ({})"
schema_info_all_fields_sql_format_oracle = """         
        select c.OWNER as TABLE_SCHEMA,
               c.TABLE_NAME,
               c.COLUMN_NAME,
               c.DATA_TYPE,
               nvl(c.DATA_PRECISION, c.DATA_LENGTH) as NUMERIC_PRECISION,
               c.DATA_SCALE as NUMERIC_SCALE,
               nvl(cc.COMMENTS, c.COLUMN_NAME) as COLUMN_COMMENT,
               c.NULLABLE as IS_NULLABLE,
               case when (select c1.constraint_type
                  from all_constraints c1, all_cons_columns cc1
                 where cc1.OWNER = c1.OWNER
                   and cc1.TABLE_NAME = c1.TABLE_NAME
                   and c1.constraint_type = 'P'
                   and c1.CONSTRAINT_NAME = cc1.CONSTRAINT_NAME
                   and c1.status = 'ENABLED'
                   and c1.OWNER = c.OWNER
                   AND cc.COLUMN_NAME = cc1.COLUMN_NAME
                   and c1.table_name = c.TABLE_NAME)='P' 
               then 'PRI' else '' end as COLUMN_KEY
          from all_tab_columns c, all_col_comments cc
         where cc.TABLE_NAME = c.TABLE_NAME
           and c.OWNER = cc.OWNER
           and c.COLUMN_NAME = cc.COLUMN_NAME
           and c.OWNER = :SCHEMA 
           and c.TABLE_NAME in ({})
         """


def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow


def get_all_table_in_the_schema(schema):
    if schema is None:
        logger.warning("get_table_info,schema should not be None")
        return None
    conn = con_oracle()
    cursor = conn.cursor()
    sql = schema_info_all_table_sql_format_oracle
    params = {}
    params["SCHEMA"] = schema
    cursor.execute(sql, params)
    cursor._cursor.rowfactory = makeDictFactory(cursor)
    result = cursor.fetchall()
    return result


def get_table_info(schema, table_name_list):
    if schema is None:
        logger.warning("get_table_info,schema should not be None")
        return None
    conn = con_oracle()
    cursor = conn.cursor()
    sql = None
    if table_name_list is None:
        sql = schema_info_all_table_sql_format_oracle
    else:
        sql = schema_info_table_sql_format_oracle
    params = {}
    params["SCHEMA"] = schema
    str_param = None
    if table_name_list is not None and len(table_name_list) > 0:
        for item in table_name_list:
            if str_param is None:
                str_param = "'" + item + "'"
            else:
                str_param += ",'" + item + "'"
        sql = sql.format(str_param)
    cursor.execute(sql, params)
    cursor._cursor.rowfactory = makeDictFactory(cursor)
    result = cursor.fetchall()
    return result


def get_table_column_info(schema, table_name_list):
    if schema is None:
        logger.warning("get_table_column_info,schema should not be None")
        return None
    if table_name_list is None:
        logger.warning("get_table_column_info,table_name should not be None")
        return None
    conn = con_oracle()
    cursor = conn.cursor()
    sql = schema_info_all_fields_sql_format_oracle
    str_param = None
    result_res = []
    if table_name_list is not None:
        iCount = len(table_name_list)
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
            list_split = table_name_list[i_from:i_to]
            for item in list_split:
                if str_param is None:
                    str_param = "'" + item + "'"
                else:
                    str_param += ",'" + item + "'"
            sql = sql.format(str_param)
            params = {}
            params["SCHEMA"] = schema
            cursor.execute(sql, params)
            cursor._cursor.rowfactory = makeDictFactory(cursor)
            result = cursor.fetchall()
            result_res += result
    return result_res


##1.初始化表和字段信息，反向从数据库
def reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list):
    tables = get_table_info(schema, tables_list)
    tab_list = []
    if tables is not None and len(tables) > 0:
        for tbl in tables:
            tab_name = tbl.get("TABLE_NAME")
            tab_list.append(tab_name)
    columns = get_table_column_info(schema, tab_list)
    re = mdr.intialize_md_tables_from_schema(user_id, tenant_id, database_name, schema, tables, columns)
    return re


if __name__ == '__main__':
    schema = "SALE_CFG"
    tables_list = None  # ["CFG_MAIN_SPART_T", "ABC"]
    # re = get_table_column_info(schema, tables)

    # ##insert the metadata of table and columns into meatadata tables
    # schema = "test"
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    database_name = "Oracle"
    # tables_list = ['roles']
    re = reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list)
    logger.info("all tables in[{}],re={}".format(schema, re))
