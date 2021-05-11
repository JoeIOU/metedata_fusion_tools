# ####metadata.py
import time, datetime
import decimal
from common.guid import get_guid
from db.db_conn import db_connection_metedata as db_md
from config.config import cfg as config
from privilege import data_privilege as dp, role_privilege as rp, user_mngt as ur
from common import constants as const

logger = config.logger
# 执行sql操作类型CRUD等
DB_EXEC_TYPE_INSERT = "INSERT"
DB_EXEC_TYPE_UPDATE = "UPDATE"
DB_EXEC_TYPE_DELETE = "DELETE"
DB_EXEC_TYPE_QUERY = "QUERY"
DB_EXEC_TYPE_VALIDATE = "VALIDATION"
# 执行sql的返回状态
DB_EXEC_STATUS_SUCCESS = 200
DB_EXEC_STATUS_FAIL = 500
DB_EXEC_STATUS_PANDING = 100
DB_EXEC_STATUS_OVERTIME = 501
# 限制查询最大数量
SIZE_LIMITED = 1001

KEY_FIELDS_ID = "$_row_id_"


# 元数据实体
def get_md_entities(tenant_id, md_entity_ids):
    if md_entity_ids is None or len(md_entity_ids) <= 0:
        logger.warning("get_md_entities,md_entity_ids is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select distinct * from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_id in %s"
    cursor.execute(sql, args=(tenant_id, md_entity_ids,))
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("get_md_entities,entitire:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# lookup数据实体
def get_lookup_items(tenant_id, lookup_codes):
    if lookup_codes is None or len(lookup_codes) <= 0:
        logger.warning("get_lookup_items,lookup_codes is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = """SELECT DISTINCT
                c.lookup_classify_id,
                c.lookup_code,
                c.lookup_name,
                c.lookup_name_en,
                c.tenant_id,
                i.lookup_item_id,
                i.lookup_item_code,
                i.lookup_item_name,
                i.lookup_item_name_en
            FROM
                lookup_classify c,
                lookup_item i
            WHERE
                c.active_flag = 'Y'
            AND c.lookup_classify_id = i.lookup_classify_id
            AND i.active_flag = 'Y'
            AND (c.tenant_id =%s or c.public_flag='Y')
            AND c.lookup_code IN %s"""
    cursor.execute(sql, args=(tenant_id, lookup_codes,))
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("get_lookup_items,result:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据实体清单list
def get_md_entities_list(tenant_id):
    conn = db_md()
    cursor = conn.cursor()
    sql = "select distinct md_entity_id,tenant_id,md_entity_name,md_entity_code,md_entity_name_en,md_entity_desc,md_tables_id " \
          "from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') limit {}".format(SIZE_LIMITED)
    cursor.execute(sql, args=(tenant_id,))
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("get_md_entities_list:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据实体通过实体code编码
def get_md_entities_by_code(tenant_id, md_entity_codes):
    if md_entity_codes is None or len(md_entity_codes) <= 0:
        logger.warning("get_md_entities_by_name,md_entity_names is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select distinct * from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_code in %s"
    cursor.execute(sql, args=(tenant_id, md_entity_codes,))
    result = cursor.fetchall()
    result = data_type_convert(result)
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
    sql = "select distinct md_entity_id,md_entity_code,md_tables_id,public_flag from md_entities where active_flag='Y' and md_entity_code in %s"
    cursor.execute(sql, args=(md_entity_codes,))
    result = cursor.fetchall()
    result = data_type_convert(result)
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
    sql = "select distinct * from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_name in %s"
    cursor.execute(sql, args=(tenant_id, md_entity_names,))
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("md_entitire:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据属性
def get_md_fields(tenant_id, md_entity_id, only_active=True):
    if md_entity_id is None:
        logger.warning("get_md_fields,md_entity_id is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    # sql = "select distinct * from md_fields where active_flag='Y' and (tenant_id=%s or public_flag='Y') and md_entity_id=%s"
    sql = """select distinct f.* from md_fields f
            inner join md_entities e on e.md_entity_id=f.md_entity_id
            where  (e.tenant_id=%s or e.public_flag='Y') and e.md_entity_id=%s"""
    if (only_active):
        sql += " and f.active_flag='Y'"
    cursor.execute(sql, args=(tenant_id, md_entity_id,))
    result = cursor.fetchall()
    result = data_type_convert(result)
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
    sql = "select distinct * from md_tables where active_flag='Y'and (tenant_id=%s or public_flag='Y') and  md_tables_id in %s"
    cursor.execute(sql, args=(tenant_id, md_table_ids,))
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("md_tables:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据DB表映射通过表名
def get_md_tables_by_name(tenant_id, md_table_names):
    conn = db_md()
    cursor = conn.cursor()
    sql = "select distinct * from md_tables where active_flag='Y' and (tenant_id=%s or public_flag='Y')"
    if md_table_names is not None and len(md_table_names) > 0:
        sql += " and  md_tables_name in %s limit {}".format(SIZE_LIMITED)
        cursor.execute(sql, args=(tenant_id, md_table_names,))
    else:
        sql += " limit {}".format(SIZE_LIMITED)
        cursor.execute(sql, args=(tenant_id,))

    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("md_tables by Name:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 元数据数据表字段映射
def get_md_columns(tenant_id, md_table_id, only_active=True):
    if md_table_id is None:
        logger.warning("get_md_columns,md_table_id is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    # sql = "select distinct * from md_columns where active_flag='Y' and (tenant_id=%s or public_flag='Y') and  md_tables_id =%s"
    sql = """select distinct c.* from md_columns c 
            INNER JOIN md_tables t on t.md_tables_id=c.md_tables_id
            where (t.tenant_id=%s or t.public_flag='Y') and  t.md_tables_id =%s
          """
    if (only_active):
        sql += " and c.active_flag='Y'"
    cursor.execute(sql, args=(tenant_id, md_table_id,))
    result = cursor.fetchall()
    result = data_type_convert(result)
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
    sql = "select distinct * from md_columns where active_flag='Y' and is_key='Y' and  md_tables_id in %s"
    cursor.execute(sql, args=(md_table_ids,))
    result = cursor.fetchall()
    result = data_type_convert(result)
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
    # sql = "select distinct * from md_entities_rel where active_flag='Y' and tenant_id=%s "
    sql = """
            SELECT DISTINCT
                e.md_entity_code from_entity_code,
                e1.md_entity_code to_entity_code,
                f.md_fields_name from_field_name,
                f1.md_fields_name to_field_name,
                r.*
            FROM
                md_entities_rel r
            INNER JOIN md_entities e ON r.from_entity_id = e.md_entity_id
            AND (
                e.tenant_id = %s
                OR e.public_flag = 'Y'
            )
            LEFT JOIN md_fields f ON r.from_field_id = f.md_fields_id
            AND f.active_flag = 'Y'
            INNER JOIN md_entities e1 ON r.to_entity_id = e1.md_entity_id
            AND (
                e1.tenant_id = %s
                OR e1.public_flag = 'Y'
            )
            LEFT JOIN md_fields f1 ON r.to_field_id = f1.md_fields_id
            AND f1.active_flag = 'Y'
            WHERE
                r.active_flag = 'Y'
        """
    if (from_entity_ids is not None and len(from_entity_ids) > 0) and (
            to_entity_ids is not None and len(to_entity_ids) > 0):
        sql += "and (r.from_entity_id in %s and r.to_entity_id in %s)"
        arg = (tenant_id, tenant_id, from_entity_ids, to_entity_ids,)
    elif (from_entity_ids is not None and len(from_entity_ids) > 0):
        sql += "and (r.from_entity_id in %s)"
        arg = (tenant_id, tenant_id, from_entity_ids,)
    elif (to_entity_ids is not None and len(to_entity_ids) > 0):
        sql += "and (r.to_entity_id in %s)"
        arg = (tenant_id, tenant_id, to_entity_ids,)
    else:
        return None
    cursor.execute(sql, args=arg)
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("md_entitire_rel:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 实体关系对应的存储表关系
def get_md_entities_rel_tables_columns(tenant_id, from_entity_id, to_entity_id):
    if from_entity_id is None and to_entity_id is None:
        logger.warning("get_md_entities_rel_tables_columns,to_entity_id and from_entity_id is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = """
            SELECT DISTINCT
                r.md_entity_rel_id,
                r.from_entity_id,
                r.rel_type,
                r.md_entity_rel_desc,
                e1.md_entity_id to_md_entity_id,
                e1.md_entity_code to_md_entity_code,
                e1.md_entity_name to_md_entity_name,
                e1.md_entity_desc to_md_entity_desc,
                e1.tenant_id to_tenant_id,
                e1.public_flag to_public_flag,
                e1.sys_flag,
                r.md_tables_id,
                t.schema_code,
                t.md_tables_name,
                r.from_columns_id,
                c.md_columns_name AS from_columns_name,
                r.to_columns_id,
                c1.md_columns_name AS to_columns_name
            FROM
                md_entities e1
            INNER JOIN md_entities_rel r ON e1.md_entity_id = r.to_entity_id
            LEFT JOIN md_tables t ON t.md_tables_id = r.md_tables_id
            AND t.active_flag = 'Y'
            LEFT JOIN md_columns c ON c.md_columns_id = r.from_columns_id
            AND c.active_flag = 'Y'
            LEFT JOIN md_columns c1 ON c1.md_columns_id = r.to_columns_id
            AND c1.active_flag = 'Y'
            WHERE
                (
                    e1.tenant_id = %s
                    OR e1.public_flag = 'Y'
                )
            
        """
    arg = (tenant_id,)
    if (from_entity_id is not None):
        sql += " AND r.from_entity_id = %s"
        arg += (from_entity_id,)
    if (to_entity_id is not None):
        sql += " AND e1.md_entity_id = %s"
        arg += (to_entity_id,)
    else:
        return None
    cursor.execute(sql, args=arg)
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("get_md_entities_rel_tables_columns:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


# 系统表的实体关系对应的存储表关系
def get_md_entities_rel_tables_columns_sys(tenant_id, from_entity_id, to_entity_id):
    if from_entity_id is None and to_entity_id is None:
        logger.warning("get_md_entities_rel_tables_columns_sys,to_entity_id and from_entity_id is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = """
            SELECT DISTINCT
                r.md_entity_rel_id,
                r.from_entity_id,
                r.rel_type,
                r.md_entity_rel_desc,
                e1.md_entity_id to_md_entity_id,
                e1.md_entity_code to_md_entity_code,
                e1.md_entity_name to_md_entity_name,
                e1.md_entity_desc to_md_entity_desc,
                e1.tenant_id to_tenant_id,
                e1.public_flag to_public_flag,
                e1.sys_flag,
                e1.md_tables_id,
                t.schema_code,
                t.md_tables_name,
                r.from_columns_id,
                c.md_columns_name AS from_columns_name,
                cc.md_columns_id AS to_columns_id,
                cc.md_columns_name AS to_columns_name
            FROM
                md_entities e1
            INNER JOIN md_entities_rel r ON e1.md_entity_id = r.to_entity_id
            LEFT JOIN md_tables t ON t.md_tables_id = e1.md_tables_id
            AND t.active_flag = 'Y'
            LEFT JOIN md_fields f ON f.md_fields_id = r.from_field_id
            AND f.active_flag = 'Y'
            LEFT JOIN md_columns c ON c.md_columns_id = f.md_columns_id
            AND c.active_flag = 'Y'
            LEFT JOIN md_fields ff ON ff.md_fields_id = r.to_field_id
            AND ff.active_flag = 'Y'
            LEFT JOIN md_columns cc ON cc.md_columns_id = ff.md_columns_id
            AND cc.active_flag = 'Y'
            WHERE
                (
                    e1.tenant_id = %s
                    OR e1.public_flag = 'Y'
                )

        """
    arg = (tenant_id,)
    if (from_entity_id is not None):
        sql += " AND r.from_entity_id = %s"
        arg += (from_entity_id,)
    if (to_entity_id is not None):
        sql += " AND e1.md_entity_id = %s"
        arg += (to_entity_id,)
    else:
        return None
    cursor.execute(sql, args=arg)
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("get_md_entities_rel_tables_columns_sys:{}".format(result))
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


# sql执行
def sql_exec(conn, sql, values):
    ls = []
    try:
        cursor = conn.cursor()
        if values is not None and len(values) > 0:
            for item in values:
                if isinstance(item, dict):
                    ls.append(tuple(item.values()))
                else:
                    continue
        cursor.executemany(sql, tuple(ls))
        sql1 = cursor._cursor._executed
        logger.info('sql_exec:%s,values:%s' % (sql1, ls))
        return cursor
    except Exception as e:
        logger.error('sql_exec error,sql:[%s],message:%s' % (sql, e))
        raise e


# sql执行
def sql_query(sql, values):
    ls = []
    conn = db_md()
    try:
        cursor = conn.cursor()
        if values is not None and len(values) > 0:
            for item in values:
                if isinstance(item, dict):
                    ls.append(tuple(item.values()))
                else:
                    continue
        # cursor.execute(sql, tuple(ls))
        cursor.executemany(sql, tuple(ls))
        # 打印
        sql = cursor._cursor._executed
        logger.info('sql_query:%s,values:%s' % (sql, ls))
        re = cursor.fetchall()
        iRowCount = cursor.rowcount
        re1 = data_type_convert(re)
        return (re1, iRowCount)
    except Exception as e:
        logger.error('sql_query error,sql:[%s],message:%s' % (sql, e))
        raise e
    finally:
        conn.close()


# 查询结果转换，主要是时间/日期转换为str
def data_type_convert(record_list):
    ls = []
    if record_list is None:
        return None
    if record_list is not None:
        for item in record_list:
            itm = {}
            for key in item.keys():
                v = item[key]
                if isinstance(v, datetime.date):
                    item[key] = str(v)
                if isinstance(v, datetime.datetime):
                    item[key] = str(v)
                # elif isinstance(v, float):
                #     item[key] = str(v)
                elif isinstance(v, decimal.Decimal):
                    item[key] = float(v)
                else:
                    continue
            ls.append(item)

    return ls


# 系统字段赋值
def set_system_fields_values(values_dict, user_id, tenant_id, md_entity_id, is_update=False, is_sys_flag=False):
    if not is_update:  # 如果不是update，要写入租户ID，实体ID，以及创建人和时间
        values_dict['tenant_id'] = tenant_id
        if not is_sys_flag:
            values_dict['md_entity_id'] = md_entity_id
        values_dict['create_by'] = user_id
        values_dict['create_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    values_dict['last_update_by'] = user_id
    values_dict['last_update_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return values_dict


def query_execute(user_id, tenant_id, md_entity_id, where_dict, parent_entity_id=None):
    irows = 0
    if md_entity_id is None or tenant_id is None:
        msg = 'query_execute,tenant_id or md_entity_id is none'
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    # guid生成
    where_list_new = []
    all_fields = get_entity_all_fields(tenant_id, [md_entity_id])
    if all_fields is None:
        msg = 'query execute warning:query fields is None.'
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    table_name = None
    exist_fields = False
    data_mapping = {}
    if all_fields is None or len(all_fields) == 0:
        msg = 'query_execute,all_fields is none'
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    entity_sys_flag = None
    public_flag = False
    public_col = None
    key_col_name = None
    for field in all_fields:
        field_name = field.get('md_fields_name')
        entity_sys_flag = field.get('sys_flag')
        is_key = field.get('is_key')
        if is_key is not None and is_key == 'Y':
            key_col_name = field.get('md_columns_name')

        if field_name is not None and field_name.lower() == 'public_flag':
            public_flag = True
            public_col = field.get('md_columns_name')
        table_name = field.get('md_tables_name')
        data_mapping[field.get('md_columns_name')] = field_name
    select_str = None
    # 非系统表，其实体关系数据时存放在关系表，查询时，把关联父ID作为条件，查询某个父实体的所有子实体。
    select_parent_field, join_str, parent_data_id = None, None, None
    if parent_entity_id is not None:
        (select_parent_field, join_str, parent_data_id) = join_relation(tenant_id, md_entity_id, parent_entity_id,
                                                                        key_col_name,
                                                                        entity_sys_flag)
    if select_parent_field is not None:
        select_str = select_parent_field
    key = None
    for key in data_mapping.keys():
        if select_str is None:
            select_str = "t." + key + " as " + data_mapping[key]
        else:
            select_str += ",t." + key + " as " + data_mapping[key]

    sql = 'SELECT {keys} FROM {table} as t '.format(keys=select_str, table=table_name)
    where_mapping = {}
    if entity_sys_flag is not None and entity_sys_flag == 'Y':
        if (parent_data_id is not None and isinstance(parent_data_id, dict) and len(parent_data_id) > 0):
            keys = parent_data_id.keys()
            key = None
            for key in keys:
                break
            where_mapping[key] = parent_data_id[key]
        sql += " WHERE "
    elif select_parent_field is not None and join_str is not None:
        if (parent_data_id is not None):
            keys = parent_data_id.keys()
            key = None
            for key in keys:
                break
            value = parent_data_id.get(key)
            join_str = join_str % (value)
        sql += join_str + " WHERE "
    else:
        sql += " WHERE "

    if where_dict is not None and len(where_dict) > 0:
        for key1 in where_dict.keys():
            field = None
            for field in all_fields:
                field_name1 = field.get('md_fields_name')
                exist_fields = False
                is_key = field.get('is_key')
                if is_key is not None and is_key == 'Y' and KEY_FIELDS_ID == key1:
                    exist_fields = True
                    break
                elif key1 == field_name1:
                    exist_fields = True
                    break
            if exist_fields:  # 有数据输入，匹配元数据实体，才赋值和引入
                v = where_dict[key1]
                k = field.get('md_columns_name')
                where_mapping[k] = v

    where_mapping['tenant_id'] = tenant_id
    # 数据权限
    dp_list = dp.query_data_privilege_info(tenant_id, user_id, md_entity_id, const.ENTITY_TYPE_ENTITY)
    # 假如是系统表，则查询时不做实体ID限制，否则，则要增加。
    if entity_sys_flag is not None and entity_sys_flag == "N":
        md_id = -1
        if md_entity_id is not None and isinstance(md_entity_id, str):
            md_id = int(md_entity_id)
        where_mapping['md_entity_id'] = md_id
    where_list_new.append(where_mapping)
    s1 = None
    for wh in where_mapping.keys():
        symbol = "="
        v = where_mapping.get(wh)
        # 有输入字符串%，则表示模糊查询
        if (wh is not None and v is not None and isinstance(v, str) and v.find('%') >= 0):
            symbol = 'like'
        elif wh is not None and v is not None and isinstance(v, list):
            symbol = 'in'
        if s1 is None:
            s1 = "t." + wh + ' {} %s'.format(symbol)
        else:
            s1 += ' and t.' + wh + ' {} %s'.format(symbol)
    if public_flag is not None and public_flag and public_col is not None:
        srep = "(t.tenant_id=%s or t." + public_col + "='Y')"
        s1 = s1.replace("t.tenant_id = %s", srep)
    sql_where = '{param}'.format(param=s1)
    sql_condition = ""
    icount = SIZE_LIMITED
    message = "Query Success"
    state = DB_EXEC_STATUS_SUCCESS
    if dp_list is None or len(dp_list) <= 0:
        message = "The user[user_id={}] have no privilege to access the entity(md_entity_id=[{}])".format(user_id,
                                                                                                          md_entity_id)
        state = DB_EXEC_STATUS_FAIL
        logger.warning(message)
        icount = 0
    else:
        for itm in dp_list:
            sql_format = itm.get("sql_format")
            if sql_format is not None and len(sql_format.strip()) > 0:
                sql_condition += " and " + sql_format

    limit_include = "select * from({sql_include})aaa LIMIT {size}"

    sql += sql_where + sql_condition
    sql = limit_include.format(sql_include=sql, size=icount)
    (re, irows) = sql_query(sql, where_list_new)
    re = exec_output_status(type=DB_EXEC_TYPE_QUERY, status=state, rows=irows, data=re,
                            message=message)
    return re


# 关联实体关系，进行元数据实体关联关系查询（如：通过父实体ID查询子实体信息）
def join_relation(tenant_id, md_entity_id, parent_entity_id, key_col_name, sys_flag):
    select_field = None
    join_str = None
    parent_data_id = None
    if parent_entity_id is not None and isinstance(parent_entity_id, dict):
        parent_key = None
        for key in parent_entity_id:
            parent_key = key
            parent_data_id = parent_entity_id.get(key)
            break

        if sys_flag is not None and sys_flag == "Y":  # 系统表，则字段直接查询关联。
            if parent_data_id is not None and key_col_name is not None:
                # select_field = ""
                res = get_md_entities_rel_tables_columns_sys(tenant_id, parent_key, md_entity_id)
                if res is not None and len(res) > 0:
                    rec = res[0]
                    parent_rel_col = rec.get("from_columns_name")
                    if parent_rel_col is not None:
                        dict1 = {}
                        dict1[parent_rel_col] = parent_data_id
                        parent_data_id = dict1
                        select_field = " t.{} as $parent_data_id ".format(parent_rel_col)
        else:
            rres = get_md_entities_rel_tables_columns(tenant_id, parent_key, md_entity_id)
            if (rres is not None and len(rres) > 0):
                item = rres[0]
                schema_code = item.get("schema_code")
                alias = "rel"
                md_entity_rel_id = item.get("md_entity_rel_id")
                rel_table_name = item.get("md_tables_name")
                from_col_name = item.get("from_columns_name")
                to_col_name = item.get("to_columns_name")
                select_field = "{}.{} as $parent_data_id ".format(alias, from_col_name)
                join_str = ' join {table} as {alias} on {alias}.md_entity_rel_id={entity_rel_id} and {alias}.{to_col_name}=t.{col}'.format(
                    table=rel_table_name, alias=alias, entity_rel_id=md_entity_rel_id,
                    to_col_name=to_col_name, col=key_col_name)
                join = ""
                if parent_data_id is not None:
                    parent_condition_str = ' and {alias}.{parent_id}=%s'.format(alias=alias, parent_id=from_col_name)
                    join_str += parent_condition_str
                    dict1 = {}
                    dict1[from_col_name] = parent_data_id
                    parent_data_id = dict1
                    join = ' inner '
                else:
                    join = ' left '

                join_str = join + join_str

        return (select_field, join_str, parent_data_id)


def insert_execute(user_id, tenant_id, md_entity_id, data_list, parent_entity_dict=None):
    irows = 0
    if md_entity_id is None or tenant_id is None:
        msg = 'insert_execute,tenant_id or md_entity_id is none'
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    # guid生成
    n = 1
    if data_list is not None and len(data_list) > 0:
        n = len(data_list)
    ids = get_guid(n)
    data_list_new = []
    id = ids[0]
    all_fields = get_entity_all_fields(tenant_id, [md_entity_id])
    if all_fields is None:
        msg = 'insert execute warning:query fields is None'
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    table_name = None
    exist_fields = False
    b_flag = False
    data_mapping = {}
    entity_relative_tables_list = []
    if isinstance(data_list, list) and len(data_list) > 0:
        count = 0
        for data_dict in data_list:
            id = ids[count]
            count += 1
            data_mapping = {}
            sys_flag = None
            for field in all_fields:
                field_name = field.get('md_fields_name')
                table_name = field.get('md_tables_name')
                sys_flag = field.get('sys_flag')
                v = None
                exist_fields = False
                if field.get('is_key') == 'Y':  # key关键字赋值，guid
                    exist_fields = True
                    v = id
                else:
                    for key in data_dict.keys():
                        if key.upper() == field_name.upper():
                            v = data_dict[key]
                            exist_fields = True
                            if table_name is not None and table_name.lower() == 'md_entities' and key.lower() == 'md_tables_id':
                                if entity_relative_tables_list.count(v) <= 0:
                                    entity_relative_tables_list.append(v)
                            break
                if exist_fields:  # 有数据输入，匹配元数据实体，才赋值和引入
                    data_mapping[field.get('md_columns_name')] = v
            b_flag = False
            if sys_flag is not None and sys_flag == 'Y':
                b_flag = True
            # 系统字段赋值
            set_system_fields_values(data_mapping, user_id, tenant_id, md_entity_id, is_sys_flag=b_flag)
            data_list_new.append(data_mapping)
    keys = ', '.join(data_mapping.keys())
    params = ', '.join(['%s'] * len(data_mapping))
    if table_name is None:
        msg = 'user_id={},md_entity_id={},the metadata table name is not exists, please fill in first.'.format(user_id,
                                                                                                               md_entity_id)
        logger.error(msg)
        res = exec_output_status(type=DB_EXEC_TYPE_INSERT, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                 message=msg)
        return res

    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table_name, keys=keys, values=params)
    conn = db_md()
    try:
        cursor = sql_exec(conn, sql, data_list_new)
        irows = cursor.rowcount
        if cursor is not None and cursor.rowcount > 0:
            message = "insert success,rows={}".format(cursor.rowcount)
            sStatus = DB_EXEC_STATUS_SUCCESS
            data = {"entity_id": md_entity_id, "ids": ids}
            logger.warning("insert entity,user=[{}],entity_id={},data:{}".format(user_id, md_entity_id, data_list_new))
        else:
            sStatus = DB_EXEC_STATUS_FAIL
            message = "insert failed"
            data = None
            logger.warning(
                "insert entity failed,user=[{}],entity_id={},data:{}".format(user_id, md_entity_id,
                                                                             data_list_new))
        re = exec_output_status(type=DB_EXEC_TYPE_INSERT, status=sStatus, rows=irows, data=data, message=message)
        conn.commit()
        if not b_flag:  # 凡是非系统表，存在实体关系的，写入关系表。
            insert_entity_relation(user_id, tenant_id, md_entity_id, ids, parent_entity_dict)
        # 插入到元数据实体表或者数据视图表，就要增加权限码；以及创建默认的实体字段，即填写不为空的字段（包括主键ID）。
        if table_name is not None and (table_name.lower() == 'md_entities' or table_name.lower() == 'data_views'):
            entity_type = const.ENTITY_TYPE_ENTITY
            if table_name.lower() == 'data_views':
                entity_type = const.ENTITY_TYPE_VIEW
            # 角色权限
            rp.insert_entity_privilege(user_id, tenant_id, entity_type, ids)
            # 数据范围权限
            dp.insert_data_privilege(user_id, tenant_id, entity_type, ids)
            # 插入默认实体字段
            if entity_type == const.ENTITY_TYPE_ENTITY:
                insert_default_fields(user_id, tenant_id, ids, entity_relative_tables_list)
        return re
    except Exception as e:
        logger.error('sql insert error,sql:[%s],message:%s' % (sql, e))
        conn.rollback()
        raise e
    finally:
        conn.close()


# 写入实体关系数据表（一般是创建子实体的时候）
def insert_entity_relation(user_id, tenant_id, md_entity_id, data_ids, parent_data_dict):
    if parent_data_dict is None or not isinstance(parent_data_dict, dict) or data_ids is None:
        logger.info(
            "insert entity relaiton,md_entity_id={},parent_data_dict={} is None or data_ids={} is None.".format(
                md_entity_id, parent_data_dict, data_ids))
        return None

    item = None
    for item in parent_data_dict:
        break
    parent_entity_id = item
    parent_data_id = parent_data_dict.get(item)
    if parent_data_id is None:
        logger.warning(
            "insert entity relaiton,md_entity_id={},parent_data_id is None.".format(
                md_entity_id))
        return None
    data_list = []
    rres = get_md_entities_rel_tables_columns(tenant_id, parent_entity_id, md_entity_id)
    re = None
    if (rres is not None and len(rres) > 0):
        item = rres[0]
        schema_code = item.get("schema_code")
        rel_type = item.get("rel_type")
        md_entity_rel_id = item.get("md_entity_rel_id")
        rel_table_name = item.get("md_tables_name")
        # from_col_name = item.get("from_columns_name")
        # to_col_name = item.get("to_columns_name")
        # select_field = "{} as $parent_data_id ".format(from_col_name)
        if rel_table_name is None:
            logger.warning(
                "insert entity relaiton,md_entity_id={},entity_code={} is None Exists.".format(
                    md_entity_id, rel_table_name))
            return None
        # 要求关系表的元数据实体名称和表名称一致
        res = get_md_entities_id_by_code([rel_table_name])
        rel_entity_id = None
        if (res is not None):
            rel_entity_id = res[0].get("md_entity_id")
        else:
            logger.warning(
                "insert entity relaiton,md_entity_id={},entity_code={} is None Exists or not Authorized.".format(
                    md_entity_id, rel_table_name))
            return None

        for id in data_ids:
            # rel_ids = get_guid(1)
            data_dict = {}
            # data_dict[KEY_FIELDS_ID] = rel_ids[0]
            data_dict["md_entity_rel_id"] = md_entity_rel_id
            # data_dict["md_entity_id"] = md_entity_id
            data_dict["rel_type"] = rel_type
            data_dict["from_data_id"] = parent_data_id
            data_dict["to_data_id"] = id
            data_dict["active_flag"] = "Y"
            set_system_fields_values(data_dict, user_id, tenant_id, md_entity_id, is_update=False, is_sys_flag=True)
            data_list.append(data_dict)
        re = insert_execute(user_id, tenant_id, rel_entity_id, data_list, parent_entity_dict=None)
    return re


# 删除实体关系数据表（一般是删除子实体的时候）
def delete_entity_relation(user_id, tenant_id, md_entity_id, data_ids):
    if data_ids is None:
        logger.info(
            "delete entity relaiton,md_entity_id={}, data_ids={} is None.".format(
                md_entity_id, data_ids))
        return None

    item = None
    data_list = []
    rres = get_md_entities_rel_tables_columns(tenant_id, None, md_entity_id)
    re = None
    if (rres is not None and len(rres) > 0):
        item = rres[0]
        # schema_code = item.get("schema_code")
        # rel_type = item.get("rel_type")
        md_entity_rel_id = item.get("md_entity_rel_id")
        rel_table_name = item.get("md_tables_name")
        if rel_table_name is None:
            logger.warning(
                "delete entity relaiton,md_entity_id={},entity_code={} is None Exists.".format(
                    md_entity_id, rel_table_name))
            return None
        # 要求关系表的元数据实体名称和表名称一致
        res = get_md_entities_id_by_code([rel_table_name])
        rel_entity_id = None
        if (res is not None):
            rel_entity_id = res[0].get("md_entity_id")
        else:
            logger.warning(
                "delete entity relaiton,md_entity_id={},entity_code={} is None Exists or not Authorized.".format(
                    md_entity_id, rel_table_name))
            return None

        for id in data_ids:
            data_dict = {}
            data_dict["md_entity_rel_id"] = md_entity_rel_id
            data_dict["to_data_id"] = id
            data_dict["tenant_id"] = tenant_id
            data_list.append(data_dict)
        re = delete_execute(user_id, tenant_id, rel_entity_id, data_list)
    return re


# 把数据表不为空的字段，插入到实体属性表，作为元数据实体的默认字段
def insert_default_fields(user_id, tenant_id, md_entity_ids, entity_relative_tables_ids_list):
    field_entity = get_md_entities_id_by_code(["md_fields"])
    if field_entity is None:
        logger.warning("insert_default_fields,the Entity[data_privileges] is NULL.")
        return None

    insert_entity_id = field_entity[0].get("md_entity_id")
    columns = get_md_columns_multi_table(tenant_id, entity_relative_tables_ids_list)

    if columns is None or len(columns) <= 0:
        logger.warning("insert_default_fields,get_md_columns_multi_table is NULL,input params={}".format(
            entity_relative_tables_ids_list))
    insert_fields_list = []
    ii = 0
    for sel_entity_id in md_entity_ids:
        table_id = entity_relative_tables_ids_list[ii]
        for item in columns:
            if item.get('md_tables_id') != table_id:
                continue
            # 系统字段，跳过
            # if item is None or item.get('md_columns_name').lower() == 'create_by' \
            #         or item.get('md_columns_name').lower() == 'create_date' \
            #         or item.get('md_columns_name').lower() == 'last_update_by' \
            #         or item.get('md_columns_name').lower() == 'last_update_date':
            #     continue
            if item is not None and (item.get('is_key') == 'Y' or item.get('is_cols_null') == 'N'):
                new_set = {}
                new_set["md_entity_id"] = sel_entity_id
                new_set["tenant_id"] = tenant_id
                new_set["md_columns_id"] = item.get("md_columns_id")
                new_set["md_fields_name"] = item.get("md_columns_name")
                new_set["md_fields_name_en"] = item.get("md_columns_name")
                new_set["md_fields_type"] = item.get("md_columns_type")
                new_set["md_fields_length"] = item.get("md_columns_length")
                new_set["md_decimals_length"] = item.get("md_dec_length")
                new_set["is_null"] = item.get("is_cols_null")
                new_set["is_indexed"] = "N"
                new_set["is_unique"] = "N"
                new_set["md_fields_desc"] = item.get("md_columns_desc")
                new_set["lookup_flag"] = "N"
                new_set["public_flag"] = "N"
                new_set["is_key"] = item.get("is_key")

                insert_fields_list.append(new_set)
        ii += 1

    re = insert_execute(user_id, tenant_id, insert_entity_id, insert_fields_list)
    logger.info('insert_default_fields,params={},insert result={}'.format(md_entity_ids, re))
    return re


def exec_output_status(type, status, rows, data, message):
    re = {}
    re["action"] = type
    re["status"] = status
    re["rows"] = rows
    re["data"] = data
    re["message"] = message
    return re


def update_execute(user_id, tenant_id, md_entity_id, data_list, where_list):
    irows = 0
    if user_id is None or tenant_id is None or md_entity_id is None:
        msg = 'update execute warning:user_id,tenant_id,md_entity_id or or more is None,user={},tenant_id={},entity_id={}'.format(
            user_id, tenant_id, md_entity_id)
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    data_list_new = []
    where_list_new = []
    values_new = []
    all_fields = get_entity_all_fields(tenant_id, [md_entity_id])
    if all_fields is None:
        msg = 'update execute warning:query fields is None,user=[{}],entity_id={}'.format(user_id, md_entity_id)
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    table_name = None
    exist_fields = False
    data_mapping = {}
    where_mapping = {}
    last_data_mapping = {}
    last_where_mapping = {}
    last_data = None
    last_where = None
    obj_list = []
    if isinstance(data_list, list) and len(data_list) > 0:
        i = 0
        for data_dict in data_list:
            where = where_list[i]
            i += 1
            data_mapping = {}
            sys_flag = None
            for field in all_fields:
                field_name = field.get('md_fields_name')
                table_name = field.get('md_tables_name')
                sys_flag = field.get('sys_flag')
                v = None
                exist_fields = False
                for key in data_dict.keys():
                    if key.upper() == field_name.upper():
                        v = data_dict[key]
                        exist_fields = True
                        break
                if exist_fields:  # 有数据输入，匹配元数据实体，才赋值和引入
                    if (field.get('is_key') != 'Y'):  # 排除key主键字作为更新值保存
                        data_mapping[field.get('md_columns_name')] = v

            where_mapping = {}
            is_key_fields_in_where = False
            for key1 in where.keys():
                v = None
                field = None
                for field in all_fields:
                    field_name1 = field.get('md_fields_name')
                    exist_fields = False
                    if field.get('is_key') == 'Y' and key1 == KEY_FIELDS_ID:  # key关键字赋值，guid
                        exist_fields = True
                        obj_list.append(where.get(key1))
                        is_key_fields_in_where = True
                        break
                    if key1.upper() == field_name1.upper():
                        if field.get('is_key') == 'Y':
                            obj_list.append(where.get(key1))
                            is_key_fields_in_where = True
                        exist_fields = True
                        break
                if exist_fields:  # 有数据输入，匹配元数据实体，才赋值和引入
                    v = where.get(key1)
                    k = field.get('md_columns_name')
                    where_mapping[k] = v
            b_flag = False
            if sys_flag is not None and sys_flag == "Y":
                b_flag = True
            # wehere条件为空，则不允许操作
            if where_mapping is None or len(where_mapping) <= 0 or len(where_mapping) < len(where):
                kk = None
                if where is not None:
                    kk = where.keys()
                msg = "更新操作警告：操作人：{}，由于输入条件参数[{}] 不匹配实体[{}]的属性或为空，不能更新操作！".format(user_id, where, md_entity_id)
                res = exec_output_status(type=DB_EXEC_TYPE_UPDATE, status=DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                         message=msg)
                logger.warning(res)
                return res
            # 系统字段赋值
            set_system_fields_values(data_mapping, user_id, tenant_id, md_entity_id, is_update=True, is_sys_flag=b_flag)
            where_mapping['tenant_id'] = tenant_id
            if not b_flag:
                where_mapping['md_entity_id'] = md_entity_id
            data_list_new.append(data_mapping)
            where_list_new.append(where_mapping)
            new_dict = dict(data_mapping, **where_mapping)
            values_new.append(new_dict)
            if last_data_mapping is None or len(last_data_mapping) <= 0:
                last_data_mapping = data_mapping
                last_data = data_dict
            if last_where_mapping is None or len(last_where_mapping) <= 0:
                last_where_mapping = where_mapping
                last_where = where

            if (last_data_mapping.keys() != data_mapping.keys() or last_where_mapping.keys() != where_mapping.keys()):
                msg = "更新操作警告：操作人：{}，批量更新实体{}，存在某个对象的输入参数[data:{},where:{}] 不匹配另外对象的参数[data:{}，where:{}]参数,不能更新！".format(
                    user_id,
                    md_entity_id,
                    last_data.keys(),
                    last_where.keys(),
                    data_dict.keys(),
                    where.keys())
                res = exec_output_status(type=DB_EXEC_TYPE_UPDATE, status=DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                         message=msg)
                logger.warning(res)
                return res

    s = None
    for item in data_mapping.keys():
        if s is None:
            s = item + '=%s'
        else:
            s += ',' + item + '=%s'
    sql = 'UPDATE {table} SET {keys}  WHERE '.format(table=table_name, keys=s)
    s1 = None
    for wh in where_mapping.keys():
        if s1 is None:
            s1 = wh + '=%s'
        else:
            s1 += ' and ' + wh + '=%s'
    sql_where = '{param}'.format(param=s1)
    sql += sql_where

    conn = db_md()
    try:
        cursor = sql_exec(conn, sql, values_new)
        irows = cursor.rowcount
        if cursor is not None and cursor.rowcount > 0:
            message = "update success,row={},input params{}".format(cursor.rowcount, where_list)
            sStatus = DB_EXEC_STATUS_SUCCESS
        else:
            sStatus = DB_EXEC_STATUS_SUCCESS
            message = "update rows=0,input params{}".format(where_list)
            where_mapping = None

        logger.warning("update entity,user=[{}],entity={},where={}".format(user_id, md_entity_id, where_list))
        logger.info("update entity,user=[{}],entity={},where={},new_values={}".format(user_id, md_entity_id, where_list,
                                                                                      values_new))
        data = {"entity_id": md_entity_id, "ids": obj_list}
        re = exec_output_status(type=DB_EXEC_TYPE_UPDATE, status=sStatus, rows=irows, data=data,
                                message=message)
        conn.commit()
        return re

    except Exception as e:
        logger.error('sql update error,sql:[%s],message:%s' % (sql, e))
        conn.rollback()
        raise e
    finally:
        conn.close()


def delete_execute(user_id, tenant_id, md_entity_id, where_list):
    irows = 0
    if user_id is None or tenant_id is None or md_entity_id is None:
        msg = 'delete execute,user_id,tenant_id,md_entity_id or or more is Null,user_id={},tenant_id={},entity_id={}'.format(
            user_id, tenant_id, md_entity_id)
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    where_list_new = []
    obj_list = []
    values_new = []
    all_fields = get_entity_all_fields(tenant_id, [md_entity_id])
    if all_fields is None:
        msg = 'delete execute warning:query fields is Null,user={},entity_id={}'.format(user_id, md_entity_id)
        logger.warning(msg)
        return exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_FAIL, rows=irows, data=None,
                                  message=msg)
    table_name = None
    exist_fields = False
    data_mapping = {}
    where_mapping = {}
    last_where_mapping = {}
    last_where = None
    b_flag = False
    if isinstance(where_list, list) and len(where_list) > 0:
        for data_dict in where_list:
            where = data_dict
            sys_flag = None
            for field in all_fields:
                # field_name = field.get('md_fields_name']
                table_name = field.get('md_tables_name')
                sys_flag = field.get('sys_flag')
                break

            where_mapping = {}
            include_key = False
            for key1 in where.keys():
                v = None
                field = None
                for field in all_fields:
                    field_name1 = field.get('md_fields_name')
                    exist_fields = False
                    if field.get('is_key') == 'Y' and key1 == KEY_FIELDS_ID:  # key关键字赋值，guid
                        obj_list.append(where.get(key1))
                        include_key = True
                        exist_fields = True
                        break
                    if key1.upper() == field_name1.upper():
                        if field.get('is_key') == 'Y':
                            obj_list.append(where.get(key1))
                            include_key = True
                        exist_fields = True
                        break
                if exist_fields:  # 有数据输入，匹配元数据实体，才赋值和引入
                    v = where.get(key1)
                    where_mapping[field.get('md_columns_name')] = v

                # 输入的fields不存在,且不是实体key，则不执行
            if where_mapping is None or len(where_mapping) <= 0 or len(where_mapping) < len(where):
                msg = "删除操作警告：操作人{},由于输入条件不满足，即输入参数[{}]不匹配实体[{}]属性[{}]或为空，不能做删除动作!".format(user_id, where,
                                                                                           where_mapping, md_entity_id)
                res = exec_output_status(type=DB_EXEC_TYPE_DELETE, status=DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                         message=msg)
                logger.warning(res)
                return res

            b_flag = False
            if sys_flag is not None and sys_flag == 'Y':
                b_flag = True

            # 系统字段赋值
            where_mapping['tenant_id'] = tenant_id
            if not b_flag:
                where_mapping['md_entity_id'] = md_entity_id
            where_list_new.append(where_mapping)
            new_dict = where_mapping
            values_new.append(new_dict)

            if last_where_mapping is None or len(last_where_mapping) <= 0:
                last_where_mapping = where_mapping
                last_where = where

            if (last_where_mapping.keys() != where_mapping.keys()):
                msg = "删除操作警告：操作人：{}，批量删除实体{}，存在某个对象的输入参数[where:{}] 不匹配另外对象的参数[where:{}]参数,不能删除！".format(
                    user_id,
                    md_entity_id,
                    last_where.keys(),
                    where.keys())
                res = exec_output_status(type=DB_EXEC_TYPE_DELETE, status=DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                         message=msg)
                logger.warning(res)
                return res

    s = None
    for item in data_mapping.keys():
        if s is None:
            s = item + '=%s'
        else:
            s += ',' + item + '=%s'
    sql = 'DELETE FROM {table}  WHERE '.format(table=table_name)
    if b_flag:  # 系统表只失效，不删除。
        sql = "UPDATE {table} SET active_flag='N' WHERE ".format(table=table_name)

    s1 = None
    for wh in where_mapping.keys():
        if s1 is None:
            s1 = wh + '=%s'
        else:
            s1 += ' and ' + wh + '=%s'
    sql_where = '{param}'.format(param=s1)
    sql += sql_where
    conn = db_md()
    try:
        if not b_flag:  # 非系统表，则要删除关系表的数据
            delete_entity_relation(user_id, tenant_id, md_entity_id, obj_list)
        cursor = sql_exec(conn, sql, values_new)
        irows = cursor.rowcount
        if cursor is not None and cursor.rowcount > 0:
            sStatus = DB_EXEC_STATUS_SUCCESS
            message = "delete success,rows={}".format(cursor.rowcount)
        else:
            sStatus = DB_EXEC_STATUS_SUCCESS
            message = "delete nothing"

        data = {"entity_id": md_entity_id, "ids": obj_list}
        logger.warning(
            "delete entity,Status:{},msg:{},user=[{}],entity_id={},data:{}".format(sStatus, message, user_id,
                                                                                   md_entity_id,
                                                                                   where_list_new))
        re = exec_output_status(type=DB_EXEC_TYPE_DELETE, status=sStatus, rows=irows, data=data,
                                message=message)
        conn.commit()
        return re

    except Exception as e:
        logger.error('sql_delete error,sql:[%s],message:%s' % (sql, e))
        conn.rollback()
        raise e
    finally:
        conn.close()


def getI18nMessages(tenant_id, message_keys):
    if message_keys is None:
        logger.warning("getI18nMessages,message_keys is None")
        return None
    result = None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select distinct * from messages where active_flag='Y' and (tenant_id=%s or public_flag='Y') and message_key in %s"
    cursor.execute(sql, args=(tenant_id, message_keys,))
    result = cursor.fetchall()
    result = data_type_convert(result)
    logger.info("getI18nMessages,result:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


def getI18nFeedbackMessages(tenant_id, message_key_string):
    message = ''
    if (message_key_string is not None):
        message = str(message_key_string)
    re = getI18nMessages(tenant_id, [message_key_string])
    if (re is not None and len(re) > 0):
        record = re[0]
        message = {}
        message['message_key'] = message_key_string
        message['messages'] = record.get('messages')
        message['messages_en'] = record.get('messages_en')
    return message


if __name__ == '__main__':
    # entity_ids = [30001, 30002, 30003]
    user = ur.get_user_tenant(1003)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")

    # get_entity_all_fields(tenant_id, entity_ids)
    datas = [{
        'text_col0': 'kiki-001',
        'text_col1': 'kiki',
        'n_col3': 25
    }, {
        'text_col0': 'goog-001',
        'text_col1': 'gogo',
        'n_col3': 101
    }]
    where1 = [{
        KEY_FIELDS_ID: 1346630691940601856
    }, {
        KEY_FIELDS_ID: 1349558259157176321
    }]
    wh1 = {
        KEY_FIELDS_ID: 1349558259157176321
    }
    entity_id = 30001

    # re=insert_execute(user_id, tenant_id, entity_id, datas)
    # re=update_execute(user_id, tenant_id, entity_id, datas, where1)
    # delete_execute(user_id, tenant_id, entity_id, where1)
    # re = query_execute(user_id, tenant_id, entity_id, wh1)
    re1 = getI18nMessages(tenant_id, ['save_success_hint'])
    logger.info(re1)
    re = getI18nFeedbackMessages(tenant_id, 'save_success_hint')
    logger.info(re)
