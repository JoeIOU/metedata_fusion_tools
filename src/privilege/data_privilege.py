# ####data_privilege.py
# 用户数据范围权限维护
from config.config import cfg as config
from privilege import user_mngt as ur
from mdata import metadata as md
from data import data_view as vw
from db.db_conn import db_connection_metedata as db_md
from common import util
from common import constants as const

logger = config.logger

sql_query_privilege_entity = """
                        SELECT
                            u.tenant_id,
                            u.user_id,
                            u.user_name,
                            u.account_number,
                            ug.group_id,
                            ug.user_group_name,
                            dp.data_privilege_id,
                            dp.data_privilege_code,
                            dp.data_privilege_type,
                            dp.data_privilege_desc,
                            dp.md_entity_id,
                            '' data_view_name,
                            me.md_entity_name,
                            me.md_entity_code
                        FROM
                            users AS u
                        LEFT JOIN user_groups_rel AS ul ON ul.active_flag = 'Y'
                        AND ul.tenant_id = u.tenant_id
                        AND ul.user_id = u.user_id
                        LEFT JOIN user_groups AS ug ON ug.active_flag = 'Y'
                        AND ug.tenant_id = u.tenant_id
                        AND ug.group_id = ul.group_id
                        LEFT JOIN data_privileges_rel AS dr ON dr.active_flag = 'Y'
                        AND dr.tenant_id = u.tenant_id
                        AND dr.group_id = ug.group_id
                        LEFT JOIN data_privileges AS dp ON dp.active_flag = 'Y'
                        AND dp.tenant_id = u.tenant_id
                        AND dp.data_privilege_id = dr.data_privilege_id
                        LEFT JOIN md_entities AS me ON me.active_flag = 'Y'
                        AND (me.tenant_id = u.tenant_id or me.public_flag='Y')
                        AND me.md_entity_id = dp.md_entity_id
                        WHERE
                            u.active_flag = 'Y'
                        AND u.tenant_id = %s
                        AND u.user_id = %s
                        and me.md_entity_id= %s
                        """

sql_query_privilege_view = """
                        SELECT
                            u.tenant_id,
                            u.user_id,
                            u.user_name,
                            u.account_number,
                            ug.group_id,
                            ug.user_group_name,
                            dp.data_privilege_id,
                            dp.data_privilege_code,
                            dp.data_privilege_type,
                            dp.data_privilege_desc,
                            dp.md_entity_id,
                            dv.data_view_name,
                            me.md_entity_name,
                            me.md_entity_code
                        FROM
                            users AS u
                        LEFT JOIN user_groups_rel AS ul ON ul.active_flag = 'Y'
                        AND ul.tenant_id = u.tenant_id
                        AND ul.user_id = u.user_id
                        LEFT JOIN user_groups AS ug ON ug.active_flag = 'Y'
                        AND ug.tenant_id = u.tenant_id
                        AND ug.group_id = ul.group_id
                        LEFT JOIN data_privileges_rel AS dr ON dr.active_flag = 'Y'
                        AND dr.tenant_id = u.tenant_id
                        AND dr.group_id = ug.group_id
                        LEFT JOIN data_privileges AS dp ON dp.active_flag = 'Y'
                        AND dp.tenant_id = u.tenant_id
                        AND dp.data_privilege_id = dr.data_privilege_id
                        LEFT JOIN data_views AS dv ON dv.active_flag = 'Y'
                        AND dv.tenant_id = u.tenant_id
                        AND dv.data_view_id = dp.md_entity_id
                        LEFT JOIN md_entities AS me ON me.active_flag = 'Y'
                        AND me.tenant_id = u.tenant_id
                        AND me.md_entity_id = dv.md_entity_id
                        WHERE
                            u.active_flag = 'Y'
                        AND u.tenant_id = %s
                        AND u.user_id = %s
                        AND dv.data_view_id  = %s
                        """
sql_query_privilege_fields_entity = """
                        SELECT dp.data_privilege_id,
                            dp.data_privilege_code,
                            dp.data_privilege_type,
                            dp.data_privilege_desc,
                            dp.md_entity_id AS object_id,
                            pf.md_fields_id,
                            pf.condition_sign,
                            pf.condition_values,
                            '' AS view_output_name,
                            f.md_entity_id,
                            f.md_fields_name,
                            f.md_fields_type,
                            f.md_columns_id,
                            c.md_columns_name
                        FROM
                            data_privileges AS dp
                        LEFT JOIN data_privilege_field AS pf ON pf.active_flag = 'Y'
                        AND pf.tenant_id = dp.tenant_id
                        AND pf.data_privilege_id = dp.data_privilege_id
                        LEFT JOIN md_fields AS f ON f.active_flag = 'Y'
                        AND f.tenant_id = dp.tenant_id
                        AND f.md_fields_id = pf.md_fields_id
                        LEFT JOIN md_columns as c on c.active_flag = 'Y'
                        and c.md_columns_id=f.md_columns_id
                        WHERE
                            dp.active_flag = 'Y'
                        AND dp.tenant_id = %s
                        AND dp.data_privilege_id in %s
                        """
sql_query_privilege_fields_view = """
                        SELECT dp.data_privilege_id,
                            dp.data_privilege_code,
                            dp.data_privilege_type,
                            dp.data_privilege_desc,
                            dp.md_entity_id AS object_id,
                            pf.md_fields_id,
                            pf.condition_sign,
                            pf.condition_values,
                            dv.view_output_name,
                            f.md_entity_id,
                            f.md_fields_name,
                            f.md_fields_type,
                            f.md_columns_id,
                            c.md_columns_name
                        FROM
                            data_privileges AS dp
                        LEFT JOIN data_privilege_field AS pf ON pf.active_flag = 'Y'
                        AND pf.tenant_id = dp.tenant_id
                        AND pf.data_privilege_id = dp.data_privilege_id
                        LEFT JOIN view_outputs AS dv ON dv.active_flag = 'Y'
                        AND dv.tenant_id = dp.tenant_id 
                        AND dv.view_output_id = pf.md_fields_id
                        LEFT JOIN md_fields AS f ON f.active_flag = 'Y'
                        AND f.tenant_id = dp.tenant_id
                        AND f.md_fields_id = dv.md_fields_id
                        LEFT JOIN md_columns as c on c.active_flag = 'Y'
                        and c.md_columns_id=f.md_columns_id
                        WHERE
                            dp.active_flag = 'Y'
                        AND dp.tenant_id = %s 
                        AND dp.data_privilege_id in %s
                        """


# 插入视图或实体的权限模型CRUD权限码数据
def insert_data_privilege(user_id, tenant_id, entity_type, md_entity_ids):
    privilege_entity=md.get_md_entities_id_by_code(["data_privileges"])
    if privilege_entity is None:
        logger.warning("insert_data_privilege,the Entity[data_privileges] is NULL.")
        return None

    insert_entity_id=privilege_entity[0].get("md_entity_id")
    if entity_type == const.ENTITY_TYPE_ENTITY:
        re = md.get_md_entities(tenant_id, md_entity_ids)
    else:
        re = vw.get_data_view(tenant_id, md_entity_ids)

    if re is None or len(re) <= 0:
        logger.warning("insert_data_privilege,get_md_entities is NULL,input params={}".format(md_entity_ids))
    data_privilege_list = []
    for item in re:
        if entity_type == const.ENTITY_TYPE_ENTITY:
            id = item.get("md_entity_id")
            str0 = str(item.get("md_entity_id")) + ":" + item.get("md_entity_name")
        else:
            id = item.get("data_view_id")
            str0 = str(item.get("data_view_id")) + ":" + item.get("data_view_name")

        new_set = {}
        new_set["md_entity_id"] = id
        new_set["tenant_id"] = tenant_id
        new_set["data_privilege_code"] = str0[:100]
        new_set["data_privilege_type"] = 'All'
        new_set["md_entity_type"] = entity_type
        new_set["data_privilege_desc"] = str0[:600]

        data_privilege_list.append(new_set)

    re = md.insert_execute(user_id, tenant_id, insert_entity_id, data_privilege_list)
    logger.info('insert_data_privilege,params={},insert result={}'.format(md_entity_ids, re))
    return re

def query_data_privilege(tenant_id, user_id, entity_id, object_type):
    sql1 = sql_query_privilege_entity
    sql2 = sql_query_privilege_view
    conn = db_md()
    cursor = conn.cursor()
    result1, result2 = None, None
    if object_type is not None and object_type == const.ENTITY_TYPE_ENTITY:
        cursor.execute(sql1, args=(tenant_id, user_id, entity_id,))
        result1 = cursor.fetchall()
    elif object_type is not None and object_type == const.ENTITY_TYPE_VIEW:
        cursor.execute(sql2, args=(tenant_id, user_id, entity_id,))
        result2 = cursor.fetchall()
    else:
        logger.warning(
            "query_data_privilege,object_type do not match,should be [View]or[Entity].userId={},entity_id={},object_type={}".format(
                user_id, entity_id, object_type))
    re = None
    if result1 is not None and len(result1) > 0:
        re = result1
    if result2 is not None and len(result2) > 0:
        if re is not None:
            re += result2
        else:
            re = result2
    logger.info("query_data_privilege,result:{}".format(re))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return re


def query_data_privilege_fields(tenant_id, privilege_ids, object_type):
    sql1 = sql_query_privilege_fields_entity
    sql2 = sql_query_privilege_fields_view
    conn = db_md()
    cursor = conn.cursor()
    result1, result2 = None, None
    if object_type is not None and object_type == const.ENTITY_TYPE_ENTITY:
        cursor.execute(sql1, args=(tenant_id, privilege_ids,))
        result1 = cursor.fetchall()
    elif object_type is not None and object_type == const.ENTITY_TYPE_VIEW:
        cursor.execute(sql2, args=(tenant_id, privilege_ids,))
        result2 = cursor.fetchall()
    else:
        logger.warning(
            "query_data_privilege,object_type do not match,should be [View]or[Entity].userId={},privilege_ids={},object_type={}".format(
                user_id, privilege_ids, object_type))

    re = None
    if result1 is not None and len(result1) > 0:
        re = result1
    if result2 is not None and len(result2) > 0:
        if re is not None:
            re += result2
        else:
            re = result2
    logger.info("query_data_privilege_fields,re:{}".format(re))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return re


def query_data_privilege_info(tenant_id, user_id, md_entity_id, object_type):
    re = query_data_privilege(tenant_id, user_id, md_entity_id, object_type)
    privilege_ids = []
    if re is None:
        logger.warning(
            'query_data_privilege_info,privilege is None,user_id={},entity_id={}'.format(user_id, md_entity_id))
        return None
    else:
        i = 0
        for item in re:
            if i >= 2000:
                break
            privilege_id = item.get("data_privilege_id")
            privilege_ids.append(privilege_id)
            i += 1
    re1 = query_data_privilege_fields(tenant_id, privilege_ids, object_type)
    set_search_condition(re1)
    logger.info('query_data_privilege_fields,result:{}'.format(re1))
    return re1


def set_search_condition(data_privilege_list):
    for item in data_privilege_list:
        # md_entity_id = item.get("md_entity_id")
        col = item.get("md_columns_name")
        sign = item.get("condition_sign")
        value = item.get("condition_values")
        sql_str = None
        if col is not None and sign is not None and value is not None:
            sign_str = util.gen_condition_sql(sign)
            str1 = sign_str % (value)
            sql_str = col + str1
        item["sql_format"] = sql_str


if __name__ == '__main__':
    user_account = "test1"
    user = ur.get_user(user_account)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    ## Entity
    md_entity_id = 30001
    re = query_data_privilege_info(tenant_id, user_id, md_entity_id,const.ENTITY_TYPE_ENTITY)

    ## View
    # md_entity_id = 50001
    # re = query_data_privilege_info(tenant_id, user_id, md_entity_id,const.ENTITY_TYPE_VIEW)
