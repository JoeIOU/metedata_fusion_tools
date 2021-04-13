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
# 执行sql的返回状态
DB_EXEC_STATUS_SUCCESS = 200
DB_EXEC_STATUS_FAIL = 500
DB_EXEC_STATUS_PANDING = 100
DB_EXEC_STATUS_OVERTIME = 501

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
    sql = "select distinct md_entity_id,tenant_id,md_entity_name,md_entity_code,md_entity_name_en,md_entity_desc,md_tables_id from md_entities where active_flag='Y' and (tenant_id=%s or public_flag='Y') limit 1000"
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
    sql = "select distinct md_entity_id,md_entity_code,md_tables_id from md_entities where active_flag='Y' and md_entity_code in %s"
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
        sql += " and  md_tables_name in %s limit 1000"
        cursor.execute(sql, args=(tenant_id, md_table_names,))
    else:
        sql += " limit 1000"
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
    result = data_type_convert(result)
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


def query_execute(user_id, tenant_id, md_entity_id, where_dict):
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
    for field in all_fields:
        field_name = field.get('md_fields_name')
        entity_sys_flag = field.get('sys_flag')
        table_name = field.get('md_tables_name')
        data_mapping[field.get('md_columns_name')] = field_name
    select_str = None
    for key in data_mapping.keys():
        if select_str is None:
            select_str = key + " as " + data_mapping[key]
        else:
            select_str += "," + key + " as " + data_mapping[key]

    sql = 'SELECT {keys} FROM {table} WHERE '.format(keys=select_str, table=table_name)
    where_mapping = {}
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
        where_mapping['md_entity_id'] = md_entity_id
    where_list_new.append(where_mapping)
    s1 = None
    for wh in where_mapping.keys():
        if s1 is None:
            s1 = wh + '=%s'
        else:
            s1 += ' and ' + wh + '=%s'
    sql_where = '{param}'.format(param=s1)
    # 限制查询最大数量1000
    icount = 1000
    sql_condition = ""
    if dp_list is None or len(dp_list) <= 0:
        logger.warning(
            "the user[user_id={}] have no privilege of the entity,md_entity_id=[{}]".format(user_id, md_entity_id))
        icount = 0
    else:
        for itm in dp_list:
            sql_format = itm.get("sql_format")
            if sql_format is not None and len(sql_format.strip()) > 0:
                sql_condition += " and " + sql_format

    limit_include = "select * from({sql_include})aaa LIMIT " + str(icount)

    sql += sql_where + sql_condition
    sql = limit_include.format(sql_include=sql)
    (re, irows) = sql_query(sql, where_list_new)
    message = "query success"
    re = exec_output_status(type=DB_EXEC_TYPE_QUERY, status=DB_EXEC_STATUS_SUCCESS, rows=irows, data=re,
                            message=message)
    return re


def insert_execute(user_id, tenant_id, md_entity_id, data_list):
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
                            if (
                                    table_name is not None and table_name.lower() == 'md_entities' and key.lower() == 'md_tables_id'):
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
            if item is None or item.get('md_columns_name').lower() == 'create_by' \
                    or item.get('md_columns_name').lower() == 'create_date' \
                    or item.get('md_columns_name').lower() == 'last_update_by' \
                    or item.get('md_columns_name').lower() == 'last_update_date':
                continue
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


def update_execute(user_id, tenant_id, md_entity_id, data_list, where_list, conn=None):
    commit_flag = True
    if conn is not None:
        commit_flag = False
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
            if where_mapping is None or len(where_mapping) <= 0 or not is_key_fields_in_where:
                kk = None
                if where is not None:
                    kk = where.keys()
                msg = "update_execute,the input condition fields[{}] is NULL or not Key Fields in the Condition or not match the fields of the entity={},by user={}.".format(
                    kk,
                    md_entity_id, user_id)
                res = exec_output_status(type=DB_EXEC_TYPE_UPDATE, status=DB_EXEC_STATUS_FAIL, rows=0,
                                         data=None,
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
        if commit_flag:
            conn.commit()
        return re

    except Exception as e:
        logger.error('sql update error,sql:[%s],message:%s' % (sql, e))
        conn.rollback()
        raise e
    finally:
        if commit_flag:
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
            for key1 in where.keys():
                v = None
                field = None
                for field in all_fields:
                    field_name1 = field.get('md_fields_name')
                    exist_fields = False
                    if field.get('is_key') == 'Y' and key1 == KEY_FIELDS_ID:  # key关键字赋值，guid
                        obj_list.append(where.get(key1))
                        exist_fields = True
                        break
                    if key1.upper() == field_name1.upper():
                        if field.get('is_key') == 'Y':
                            obj_list.append(where.get(key1))
                        exist_fields = True
                        break
                if exist_fields:  # 有数据输入，匹配元数据实体，才赋值和引入
                    v = where.get(key1)
                    where_mapping[field.get('md_columns_name')] = v
                else:  # 输入的fields不存在,且不是实体key，则不执行
                    if key1 != "md_entity_id":
                        msg = "delete_execute,the input field[{}] is not exists".format(key1)
                        res = exec_output_status(type=DB_EXEC_TYPE_DELETE, status=DB_EXEC_STATUS_FAIL, rows=0,
                                                 data=None,
                                                 message=msg)
                        logger.warning(res)
                        return res

            b_flag = False
            if sys_flag is not None and sys_flag == 'Y':
                b_flag = True
            if where_mapping is None or len(where_mapping) <= 0:
                kk = None
                if where is not None:
                    kk = where.keys()
                msg = "delete_execute,the input fields[{}] is NULL or not match the fields of the entity={},by user={}.".format(
                    kk,
                    md_entity_id, user_id)
                res = exec_output_status(type=DB_EXEC_TYPE_DELETE, status=DB_EXEC_STATUS_FAIL, rows=0,
                                         data=None,
                                         message=msg)
                logger.warning(res)
                return res

            # 系统字段赋值
            where_mapping['tenant_id'] = tenant_id
            if not b_flag:
                where_mapping['md_entity_id'] = md_entity_id
            where_list_new.append(where_mapping)
            new_dict = where_mapping
            values_new.append(new_dict)

    s = None
    for item in data_mapping.keys():
        if s is None:
            s = item + '=%s'
        else:
            s += ',' + item + '=%s'
    sql = 'DELETE FROM {table}  WHERE '.format(table=table_name)
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


if __name__ == '__main__':
    # entity_ids = [30001, 30002, 30003]
    user = ur.get_user_tenant(1001)
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
    re = query_execute(user_id, tenant_id, entity_id, wh1)
    logger.info(re)
