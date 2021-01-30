# ####data_view.py
# 数据视图查询，根据元数据生成sql查询数据和返回视图结果
from db.db_conn import db_connection_metedata as db_md
from mdata import metadata as md
from config.config import cfg as config
from privilege import data_privilege as dp, user_mngt as ur
from common import util
from common import constants as const

logger = config.logger
# between...and多值分隔标识符号
STR_SUFF = "::"

sql_in = """
            SELECT
            'input' AS io_type,
            d.data_view_id AS view_id,
            d.md_main_entity_id,
            i.md_entity_id,
            i.md_fields_id,
            i.view_input_id AS param_id,
            i.view_input_name AS view_param_name,
            i.compute_sign
        FROM
            data_views AS d
        LEFT JOIN view_inputs AS i ON i.data_view_id = d.data_view_id
        AND i.active_flag = 'Y'
        LEFT JOIN md_fields AS f ON f.active_flag = 'Y'
        AND f.md_fields_id = i.md_fields_id
        AND d.tenant_id = f.tenant_id
        WHERE
            d.active_flag = 'Y'
        AND d.tenant_id = %s
        AND d.data_view_id = %s
        """
sql_out = """
            SELECT
                'output' AS io_type,
                d.data_view_id AS view_id,
                d.md_main_entity_id,
                i.md_entity_id,
                i.md_fields_id,
                i.view_output_id,
                i.view_output_name
            FROM
                data_views AS d
            LEFT JOIN view_outputs AS i ON i.data_view_id = d.data_view_id
            AND i.active_flag = 'Y'
            LEFT JOIN md_fields AS f ON f.active_flag = 'Y'
            AND f.md_fields_id = i.md_fields_id
            AND d.tenant_id = f.tenant_id
            WHERE
                d.active_flag = 'Y'
            AND d.tenant_id = %s
            AND d.data_view_id = %s 
            """


def query_view_format(user_id, data_view_id):
    conn = db_md()
    cursor = conn.cursor()
    user = ur.get_user_tenant(user_id)
    tenant_id = user.get("tenant_id")

    if tenant_id is None:
        logger.warning('query_view,the tenant_id of the user[{}] is None.'.format(user))
        return None, None
    created_sql = None
    input_params_list = None
    cursor.execute(sql_in,
                   args=(tenant_id, data_view_id,))
    result_in = cursor.fetchall()
    cursor.execute(sql_out,
                   args=(tenant_id, data_view_id,))
    result_out = cursor.fetchall()
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    logger.info('query_view input param:\n{}'.format(result_in))
    logger.info('query_view output param:\n{}'.format(result_out))

    if not (result_in is not None and len(result_out) > 0):
        logger.warning('query_view output param is none.')
        return None
    if result_out is not None and len(result_out) > 0:
        main_entity_id = result_out[0].get("md_main_entity_id")
    else:
        main_entity_id = result_in[0].get("md_main_entity_id")
    entity_selected_list = find_entity_list(result_in, result_out)
    entity_ids = []
    for x in entity_selected_list:
        entity_ids.append(x.get('md_entity_id'))
    entities_rels = md.get_md_entities_rel(tenant_id, entity_ids, entity_ids)
    entity_table_mapping = md.get_entity_table_mapping(tenant_id, entity_ids)
    if entities_rels is None or len(entities_rels) <= 0:
        return None
    all_entity_fields = md.get_entity_all_fields(tenant_id, entity_ids)
    # 数据权限
    dp_list = dp.query_data_privilege_info(tenant_id, user_id, data_view_id, const.ENTITY_TYPE_VIEW)
    # 无权限访问，则返回
    if dp_list is not None and len(dp_list) > 0:
        logger.info("the user[{}] have some privilege,list={}".format(user_id, dp_list))
    else:
        logger.warning("the user[{}] have no privilege of the view,view id=[{}]".format(user_id, data_view_id))
        return None, None
    table_list = []
    for itm001 in entities_rels:
        tab_id = itm001.get("md_tables_id")
        if tab_id is not None and table_list.count(tab_id) <= 0:
            table_list.append(tab_id)
    rl_tables_fields = None
    if table_list is not None and len(table_list) > 0:
        rl_tables_fields = md.get_table_all_columns(tenant_id, table_list)
    for item0 in entities_rels:
        if item0.get("md_tables_id") is None:
            for itm in all_entity_fields:
                if item0.get("from_field_id") == itm.get("md_fields_id"):
                    item0['md_tables_name'] = itm.get('md_tables_name')
                    item0['from_columns_name'] = itm.get('md_columns_name')
                    break
            for itm1 in all_entity_fields:
                if item0.get("to_field_id") == itm1.get("md_fields_id"):
                    item0['to_columns_id'] = itm1.get('md_columns_id')
                    item0['to_md_tables_name'] = itm1.get('md_tables_name')
                    item0['to_columns_name'] = itm1.get('md_columns_name')
                    break
        else:
            for r_item in rl_tables_fields:
                if item0.get('from_columns_id') == r_item.get('md_columns_id'):
                    item0['md_tables_name'] = r_item.get('md_tables_name')
                    item0['from_columns_name'] = r_item.get('md_columns_name')
                    break
            for r_item1 in rl_tables_fields:
                if item0.get('to_columns_id') == r_item1.get('md_columns_id'):
                    item0['to_md_tables_name'] = r_item1.get('md_tables_name')
                    item0['to_columns_name'] = r_item1.get('md_columns_name')
                    break

    entities_rels_new = entity_sort(main_entity_id, entities_rels)
    logger.info('all_entity_fields:{}'.format(all_entity_fields))
    created_sql, input_params_list = query_view_sql_create(main_entity_id, entities_rels_new, entity_table_mapping,
                                                           all_entity_fields,
                                                           result_in,
                                                           result_out, dp_list)

    logger.info('created_sql:{}'.format(created_sql))
    return created_sql, input_params_list


def entity_sort(main_entity_id, list):
    new_list = []
    tmp_list = list.copy()
    for item in list:
        if item.get('from_entity_id') == main_entity_id:
            new_list.append(item)
            tmp_list.remove(item)
    # 如果主的找不到，则随意随意选择一个相关的从关系作为主。
    if len(new_list) <= 0:
        for item in list:
            if item.get('to_entity_id') == main_entity_id:
                new_list.append(item)
                tmp_list.remove(item)
                break
    i = 0
    if tmp_list is not None and len(tmp_list) > 0:
        while i < 10:
            li = tmp_list.copy()
            i += 1
            if li is not None and len(li) > 0:
                for im in li:
                    remain_item = im.get('from_entity_id')
                    for item in new_list:
                        if remain_item == item.get('from_entity_id'):
                            new_list.append(im)
                            tmp_list.remove(im)
                            break
            else:
                break

            li = tmp_list.copy()
            if li is not None and len(li) > 0:
                for im in li:
                    remain_item = im.get('from_entity_id')
                    for item in new_list:
                        if remain_item == item.get('to_entity_id'):
                            new_list.append(im)
                            tmp_list.remove(im)
                            break
            else:
                break
    return new_list


def query_view_sql_create(main_entity_id, entities_rels, entity_table_mapping, entity_fields_columns_list,
                          input_params,
                          output_params, dp_list):
    re = None
    from_format_sql = ' from {table} as {alias}'
    if entity_table_mapping is None or main_entity_id is None:
        return re
    main_entity = {}
    i = 1
    alias_list_conbined = []
    main_table_alias = 't'
    for item in entity_table_mapping:
        if item.get('md_entity_id') == main_entity_id:
            item['alias'] = main_table_alias
            main_entity = item
        else:
            alias = 't' + str(i)
            item['alias'] = alias
            i += 1

    main_table = main_entity.get('md_tables_name')
    tenant_id = main_entity.get('tenant_id')
    from_sql = from_format_sql.format(table=main_table, alias=main_table_alias)
    alias_list_conbined.append(main_table_alias)

    rel_table_flag = None
    for item in entities_rels:
        # from主关系查询
        if main_entity_id == item.get("from_entity_id"):
            # 关系表字段为空，则认为是没有中间表的关系，两个实体表间直连
            rel_table_flag = item.get('md_tables_id')
            break
    if rel_table_flag is None:
        for item in entities_rels:
            # to从属关系查询
            if main_entity_id == item.get("to_entity_id"):
                # 关系表字段为空，则认为是没有中间表的关系，两个实体表间直连
                rel_table_flag = item.get('md_tables_id')
                break
    where_sql, input_params_list = where_format(tenant_id, main_entity_id, input_params, entity_table_mapping,
                                                entity_fields_columns_list, rel_table_flag, main_table_alias)
    privi_sql = privi_sql_format(entity_table_mapping, dp_list)
    selected_sql = select_sql_format(entity_table_mapping, entity_fields_columns_list, output_params)
    join_sql = join_sql_format(tenant_id, main_entity_id, entities_rels, entity_table_mapping,
                               entity_fields_columns_list, alias_list_conbined)
    output_str = selected_sql + from_sql + join_sql + where_sql + privi_sql
    return output_str, input_params_list


def join_sql_format(tenant_id, main_entity_id, entities_rels, entity_table_mapping, entity_fields_columns_list,
                    alias_list_conbined):
    join_format_sql = ' join {join_table} as {join_alias} on {join_conditions}'
    join_left_format_sql = ' left' + join_format_sql
    on_format_sql = "{from_alias}.{from_column}={to_alias}.{to_column}"
    join_sql = ''
    ii = 0
    rel_table_id = None
    for item in entities_rels:
        from_entity_id = item.get('from_entity_id')
        from_fields_id = item.get('from_field_id')
        to_entity_id = item.get('to_entity_id')
        to_fields_id = item.get('to_field_id')

        rel_table_id = item.get('md_tables_id')
        rel_table_name = item.get('md_tables_name')
        rel_from_cloumns_name = item.get('from_columns_name')
        rel_to_cloumns_name = item.get('to_columns_name')
        ii += 1
        r_alias = 'r' + str(ii)
        i = 0
        to_table = None
        to_alias = None
        from_table = None
        from_alias = None
        to_key_name = None
        for item0 in entity_table_mapping:
            if from_entity_id == item0.get('md_entity_id'):
                from_alias = item0.get('alias')
                from_table = item0.get('md_tables_name')
                break
        for item0 in entity_table_mapping:
            if to_entity_id == item0.get('md_entity_id'):
                to_alias = item0.get('alias')
                to_table = item0.get('md_tables_name')
                break

        i = 0
        from_key_name = None
        for item1 in entity_fields_columns_list:
            if item1.get('md_fields_id') == from_fields_id:
                from_key_name = item1.get('md_columns_name')
                break

        for item2 in entity_fields_columns_list:
            if item2.get('md_fields_id') == to_fields_id:
                to_key_name = item2.get('md_columns_name')
                break
        # 如果主次对象查询顺序颠倒，则要调整join关系主次。
        if main_entity_id == to_entity_id:
            tmp_from_alias = from_alias
            tmp_from_key_name = from_key_name
            tmp_from_entity_id = from_entity_id
            tmp_from_table = from_table
            from_alias = to_alias
            from_key_name = to_key_name
            # from_entity_id = to_entity_id
            from_table = to_table
            to_entity_id = tmp_from_entity_id
            to_alias = tmp_from_alias
            to_key_name = tmp_from_key_name
            to_table = tmp_from_table
        # table_id为空，则认为是两个实体直接对接，不存在中间表关联
        if rel_table_id is None:
            # left
            con_str = ' {alias}.tenant_id={tenant_id} '.format(
                alias=to_alias, tenant_id=tenant_id)
            condition_str1 = on_format_sql.format(from_alias=from_alias,
                                                  from_column=from_key_name,
                                                  to_alias=to_alias,
                                                  to_column=to_key_name)
            condition_str = con_str + " and " + condition_str1
            is_exists = False
            if alias_list_conbined is not None:
                for alias_item in alias_list_conbined:
                    if to_alias.upper() == alias_item.upper():
                        is_exists = True
                        break
            if is_exists:
                join_sql_left = " and " + condition_str1
            else:
                join_sql_left = join_left_format_sql.format(join_table=to_table, join_alias=to_alias,
                                                            join_conditions=condition_str)

            join_sql += join_sql_left
            alias_list_conbined.append(to_alias)
        else:
            # left
            con_str = ' {alias}.tenant_id={tenant_id} and {alias}.md_entity_id={md_entity_id}'.format(
                alias=to_alias, tenant_id=tenant_id, md_entity_id=to_entity_id)
            condition_str = con_str
            join_sql_left = join_left_format_sql.format(join_table=to_table, join_alias=to_alias,
                                                        join_conditions=condition_str)

            join_sql += join_sql_left
            # join
            condition_str1 = on_format_sql.format(from_alias=from_alias,
                                                  from_column=from_key_name,
                                                  to_alias=r_alias,
                                                  to_column=rel_from_cloumns_name)
            condition_str2 = on_format_sql.format(from_alias=r_alias,
                                                  from_column=rel_to_cloumns_name,
                                                  to_alias=to_alias,
                                                  to_column=to_key_name)
            condition_str = condition_str1 + ' and ' + condition_str2
            is_exists = False
            is_exists1 = False
            if alias_list_conbined is not None:
                for alias_item in alias_list_conbined:
                    if to_alias.upper() == alias_item.upper():
                        is_exists = True
                        break
            if alias_list_conbined is not None:
                for alias_item in alias_list_conbined:
                    if r_alias.upper() == alias_item.upper():
                        is_exists1 = True
                        break
            if is_exists and is_exists1:
                join_sql_str = " and " + condition_str
            else:
                join_sql_str = join_left_format_sql.format(join_table=rel_table_name, join_alias=r_alias,
                                                           join_conditions=condition_str)
            join_sql += join_sql_str
            alias_list_conbined.append(to_alias)
            alias_list_conbined.append(r_alias)
    return join_sql


# select sql format
def select_sql_format(entity_table_mapping, entity_fields_columns_list, output_params):
    select_format_sql = 'select distinct {fields}'
    selected_cols = []
    for out_item in output_params:
        alias_selected = ''
        for item in entity_table_mapping:
            alias_selected = ''
            if item.get('md_entity_id') == out_item.get('md_entity_id'):
                alias_selected = item.get('alias')
                break
        if alias_selected is not None and len(alias_selected) > 0:
            for col in entity_fields_columns_list:
                if out_item.get('md_fields_id') == col.get('md_fields_id'):
                    selected_col = alias_selected + '.' + col.get('md_columns_name') + ' as ' + out_item.get(
                        'view_output_name')
                    selected_cols.append(selected_col)
                    break
    str1 = ','.join(selected_cols)
    selected_sql = select_format_sql.format(fields=str1)
    return selected_sql


# 权限sql条件生成
def privi_sql_format(entity_table_mapping, dp_list):
    privi_sql = ''
    if dp_list is not None and len(dp_list) > 0:
        for dp_item in dp_list:
            for tabl in entity_table_mapping:
                if dp_item.get("md_entity_id") == tabl.get("md_entity_id"):
                    alias_tmp = tabl.get("alias")
                    sql_format = dp_item.get("sql_format")
                    if sql_format is not None and len(sql_format.strip()) > 0:
                        s = ' and {}.' + sql_format
                        privi_sql += s.format(alias_tmp)
                    break
    else:
        privi_sql = " LIMIT 0"
    return privi_sql


# where 条件生成
def where_format(tenant_id, main_entity_id, input_params, entity_table_mapping, entity_fields_columns_list,
                 rel_table_flag, main_table_alias):
    where_format_sql = ' where {where}'
    where_sql = ''
    selected_cols = []
    input_params_list = []
    for in_item in input_params:
        alias_selected = ''
        for item in entity_table_mapping:
            alias_selected = ''
            if item.get('md_entity_id') == in_item.get('md_entity_id'):
                alias_selected = item.get('alias')
                break
        if alias_selected is not None and len(alias_selected) > 0:
            for col in entity_fields_columns_list:
                if in_item.get('md_fields_id') == col.get('md_fields_id'):
                    sign_flag = in_item.get('compute_sign')
                    s = util.gen_condition_sql(sign_flag)
                    input_param = in_item.get('view_param_name')
                    ss = "%s"
                    if s is not None and s.count(ss) > 1:
                        s_count = s.count(ss)
                        for i in range(s_count):
                            input_params_list.append(input_param + STR_SUFF + str(i))
                    else:
                        input_params_list.append(input_param)
                    selected_col = '(' + alias_selected + '.' + col.get('md_columns_name') + s + ')'
                    selected_cols.append(selected_col)
                    break
    if selected_cols is not None and len(selected_cols) > 0:
        str1 = ' and '.join(selected_cols)
        where_sql = where_format_sql.format(where=str1)
    else:
        where_sql = where_format_sql.format(where='1=1')

    if rel_table_flag is None:
        where_sql += ' and {alias}.tenant_id={tenant_id}'.format(
            alias=main_table_alias, tenant_id=tenant_id)
    else:
        where_sql += ' and {alias}.tenant_id={tenant_id} and {alias}.md_entity_id={md_entity_id}'.format(
            alias=main_table_alias, tenant_id=tenant_id, md_entity_id=main_entity_id)
    return where_sql, input_params_list


def find_main_entity_id(list):
    s_table = None
    if list is None:
        return s_table
    for item in list:
        if item.get('md_main_entity_id') == item.get('md_entity_id'):
            s_table = item.get('md_main_entity_id')
            break
    logger.info('find_main_entity_id:\n{}'.format(s_table))
    return s_table


def find_entity_list(list_in, list_out):
    s_table = None
    if list is None:
        return s_table
    list_entity = []
    for item in list_in:
        entity_dict = {}
        entity_dict['md_entity_id'] = item.get('md_entity_id')
        if list_entity.count(entity_dict) <= 0:
            list_entity.append(entity_dict)
        else:
            continue

    for item in list_out:
        entity_dict = {}
        entity_dict['md_entity_id'] = item.get('md_entity_id')
        if list_entity.count(entity_dict) <= 0:
            list_entity.append(entity_dict)
        else:
            continue
    logger.info('find_entity_list:\n{}'.format(list_entity))
    return list_entity


# 元数据视图查询
def get_data_view(tenant_id, view_ids):
    if view_ids is None or len(view_ids) <= 0:
        logger.warning("get_data_view,view_ids is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    # str1 = ",".join(str(i) for i in view_ids)
    sql = "select * from data_views where active_flag='Y' and tenant_id=%s and data_view_id in %s"
    cursor.execute(sql, args=(tenant_id, view_ids,))
    result = cursor.fetchall()
    logger.info("get_data_view,views:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


def query_view(user_id, view_id=0, input_param=None):
    sql, input_params_list = query_view_format(user_id, view_id)
    if sql is None or len(sql) <= 0:
        logger.warning('query view,format sql is NULL,view_id={}'.format(view_id))
        return None
    if input_param is not None and not isinstance(input_param, dict):
        logger.warning('query view,format input_param is not dict ,view_id={}'.format(view_id))
        return None

    ls_param_new = {}
    if input_params_list is not None and isinstance(input_params_list, list):
        for param in input_params_list:
            if param is not None and param.count(STR_SUFF) > 0:
                param1 = param[:param.index(STR_SUFF)]
            else:
                param1 = param
            for key in input_param.keys():
                if key is not None and key.count(STR_SUFF) > 0:
                    key1 = key[:key.index(STR_SUFF)]
                else:
                    key1 = key
                if key1.upper() == param1.upper():
                    ls_param_new[param] = input_param.get(key)
                    input_param.pop(key)
                    break
    key_ls = []
    for key in input_param.keys():
        val = None
        if key is not None and key.count(STR_SUFF) > 0:
            val = ls_param_new.get(key[:key.index(STR_SUFF)])
        else:
            val = ls_param_new.get(key)
        if val is None:
            key_ls.append(key)
    if len(key_ls) > 0:
        logger.warning('query view,format input_param is not match the metedata ,params={}'.format(key_ls))
        return None

    where_list = []
    where_list.append(ls_param_new)
    sql_new = "select * from ({sql_format})aaa  LIMIT 5000".format(sql_format=sql)
    logger.info('query view sql:{}'.format(sql_new))
    status = md.DB_EXEC_STATUS_SUCCESS
    message = "query success"
    try:
        (re, irows) = md.sql_query(sql_new, where_list)
        output = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=status, rows=irows, data=re, message=message)
        return output
    except Exception as e:
        logger.error('sql_query error,sql:[%s],message:%s' % (sql, e))
        status = md.DB_EXEC_STATUS_FAIL
        message = "query failed"
        irows = 0
        output = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=status, rows=irows, data=None,
                                       message=message)
        return output


if __name__ == '__main__':
    ## 业务数据测试data Test
    # # in(%s)
    # param = {"name1": ['abc', 'bb'], "name2": 'dfd33'}
    # # between %s and %s

    param = {"name1::1": 'abc', "name1::2": 'bb', "name2": 'dfd33'}
    user = ur.get_user("test1")
    qr = query_view(user["user_id"], 50001, param)
    logger.info('view result:{}'.format(qr))

    ## 元数据view测试
    param = {"teant_name_label": '%租户%', 'dept_name': '租户管理部门1'}
    user = ur.get_user("admin")
    qr = query_view(user["user_id"], 50002, param)
    logger.info('view result:{}'.format(qr))
