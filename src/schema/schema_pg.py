# ####schema_pg.py
# postgreSQL数据库表反向工程，生成元数据存入表。
from config.config import cfg as config
from db.db_conn import db_connection_pg as con_pg
from schema import metadata_eng_reverse as mdr
from privilege import user_mngt as ur

logger = config.logger

sql_pg_all_tables_in_schema = """
        SELECT
            s.nspname AS TABLE_SCHEMA,
            c.relname AS TABLE_NAME,
            COALESCE (
                cast(
                    obj_description (c.relfilenode, 'pg_class') AS VARCHAR
                ),
                c.relname
            ) AS TABLE_COMMENT
        FROM
            pg_class c
        LEFT JOIN pg_namespace s ON s.oid = c.relnamespace
        WHERE
            c.relkind = 'r'
        AND s.nspname = %s        
	    """
sql_pg_tables = sql_pg_all_tables_in_schema + " AND c.relname in ({})"

sql_pg_table_columns = """
        SELECT
            s.nspname AS TABLE_SCHEMA,
            c.relname AS TABLE_NAME,
            a.attname AS COLUMN_NAME,
            t.typname AS DATA_TYPE,
         CASE a.atttypid
        WHEN 21 /*int2*/THEN	16
        WHEN 23 /*int4*/THEN	32
        WHEN 20 /*int8*/THEN	64
        WHEN 1700 /*numeric*/THEN
            CASE WHEN a.atttypmod = - 1 THEN	NULL
          ELSE	((a.atttypmod - 4) >> 16) & 65535 -- calculate the precision  
          END
        WHEN 700 /*float4*/THEN	24 /*FLT_MANT_DIG*/
        WHEN 701 /*float8*/THEN	53 /*DBL_MANT_DIG*/
        ELSE
            CASE
          WHEN a.attlen > 0 THEN	a.attlen
          ELSE
              a.atttypmod - 4
          END
        END AS NUMERIC_PRECISION,
         CASE
        WHEN a.atttypid IN (21, 23, 20) THEN
            0
        WHEN a.atttypid IN (1700) THEN
            CASE
        WHEN a.atttypmod = - 1 THEN
            NULL
        ELSE
            (a.atttypmod - 4) & 65535 -- calculate the scale    
        END
        ELSE  NULL
        END AS NUMERIC_SCALE,
         b.description AS COLUMN_COMMENT,
         CASE
        WHEN a.attnotnull = 't' THEN
            'N'
        ELSE
            'Y'
        END AS IS_NULLABLE,
         CASE
        WHEN cs.contype = 'p' THEN
            'PRI'
        ELSE NULL
        END AS COLUMN_KEY
        FROM
            pg_attribute a
        LEFT JOIN pg_class c ON a.attrelid = c.oid
        LEFT JOIN pg_description b ON a.attrelid = b.objoid
        AND a.attnum = b.objsubid
        LEFT JOIN pg_namespace s ON s.oid = c.relnamespace
        AND a.attnum = b.objsubid
        LEFT JOIN pg_type t ON a.atttypid = t.oid
        LEFT JOIN pg_constraint cs ON cs.conrelid = c.oid
        AND a.attnum = cs.conkey [ 1 ]
        AND cs.contype = 'p'
        WHERE s.nspname=%s
            AND	c.relname in ({})
            AND a.attnum > 0
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
    conn = con_pg()
    cursor = conn.cursor()
    sql = sql_pg_all_tables_in_schema
    params = {}
    # params["SCHEMA"] = schema
    cursor.execute(sql, [schema])
    result = fetch_result_2_dict(cursor)
    return result


def fetch_result_2_dict(cursor):
    result = None
    if cursor is None:
        return result
    # 获取表的所有字段名称
    coloumns = [row[0].upper() for row in cursor.description]
    rows = [[item for item in row] for row in cursor.fetchall()]
    result = [dict(zip(coloumns, row)) for row in rows]
    return result


def get_table_info(schema, table_name_list):
    if schema is None:
        logger.warning("get_table_info,schema should not be None")
        return None
    conn = con_pg()
    cursor = conn.cursor()
    sql = None
    if table_name_list is None:
        sql = sql_pg_all_tables_in_schema
    else:
        sql = sql_pg_tables
    # params = {}
    # params["SCHEMA"] = schema
    str_param = None
    if table_name_list is not None and len(table_name_list) > 0:
        for item in table_name_list:
            if str_param is None:
                str_param = "'" + item + "'"
            else:
                str_param += ",'" + item + "'"
        sql = sql.format(str_param)
    cursor.execute(sql, [schema])
    result = fetch_result_2_dict(cursor)
    return result


def get_table_column_info(schema, table_name_list):
    if schema is None:
        logger.warning("get_table_column_info,schema should not be None")
        return None
    if table_name_list is None:
        logger.warning("get_table_column_info,table_name should not be None")
        return None
    conn = con_pg()
    cursor = conn.cursor()
    sql = sql_pg_table_columns
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
            # params = {}
            # params["SCHEMA"] = schema
            cursor.execute(sql, [schema])
            result = fetch_result_2_dict(cursor)
            if result is not None:
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
    schema = "test"
    tables_list = None  # ["CFG_MAIN_SPART_T", "ABC"]
    # re = get_table_column_info(schema, tables)

    # ##insert the metadata of table and columns into meatadata tables
    # schema = "test"
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    database_name = "PG_TEST"
    # tables_list = ['roles']
    re = reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list)
    logger.info("all tables in[{}],re={}".format(schema, re))
