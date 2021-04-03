# ####role_privilege.py
# 用户角色和权限维护
from config.config import cfg as config
from mdata import metadata as md
from privilege import user_mngt as ur
from data import data_view as vw
from db.db_conn import db_connection_metedata as db_md
from common import constants as const

logger = config.logger
privilege_list = []
privilege_list.append(const.PRIVILEGE_TYPE_CREATE)
privilege_list.append(const.PRIVILEGE_TYPE_UPDATE)
privilege_list.append(const.PRIVILEGE_TYPE_READ)
privilege_list.append(const.PRIVILEGE_TYPE_DELETE)

sql_query_privilege = """
                SELECT
                    u.tenant_id,
                    u.user_id,
                    u.user_name,
                    u.account_number,
                    rs.role_name,
                    ur.user_role_desc,
                    ep.md_entity_id,
                    ep.entity_type,
                    ep.privilege_type,
                    ep.privilege_code
                FROM
                    users AS u
                LEFT JOIN user_roles AS ur ON ur.user_id = u.user_id
                AND ur.active_flag = 'Y'
                AND ur.tenant_id = u.tenant_id
                LEFT JOIN roles AS rs ON rs.role_id = ur.role_id
                AND rs.active_flag = 'Y'
                AND u.tenant_id = rs.tenant_id
                LEFT JOIN role_privileges AS r ON r.role_id = ur.role_id
                AND r.active_flag = 'Y'
                AND u.tenant_id = r.tenant_id
                LEFT JOIN entity_privileges AS ep ON ep.entity_privilege_id = r.entity_privilege_id
                AND ep.active_flag = 'Y'
                AND ep.tenant_id = u.tenant_id
                WHERE
                    u.active_flag = 'Y'
                AND u.tenant_id = %s
                AND u.user_id = %s
                LIMIT 5000
"""


# 插入视图或实体的权限模型CRUD权限码数据
def insert_entity_privilege(user_id, tenant_id, entity_type, md_entity_ids):
    privilege_entity=md.get_md_entities_id_by_code(["entity_privileges"])
    if privilege_entity is None:
        logger.warning("insert_entity_privilege,the Entity[entity_privileges] is NULL.")
        return None

    insert_entity_id=privilege_entity[0].get("md_entity_id")
    if entity_type == const.ENTITY_TYPE_ENTITY:
        re = md.get_md_entities(tenant_id, md_entity_ids)
    else:
        re = vw.get_data_view(tenant_id, md_entity_ids)

    if re is None or len(re) <= 0:
        logger.warning("insert_entity_privilege,get_md_entities is NULL,input params={}".format(md_entity_ids))
    entity_privilege_list = []
    for item in re:
        if entity_type == const.ENTITY_TYPE_ENTITY:
            id = item.get("md_entity_id")
            str0 = str(item.get("md_entity_id")) + ":" + item.get("md_entity_name")
        else:
            id = item.get("data_view_id")
            str0 = str(item.get("data_view_id")) + ":" + item.get("data_view_name")

        for code in privilege_list:
            if entity_type == const.ENTITY_TYPE_VIEW:
                # view视图只有Read权限，没有Create/Update/Delete权限
                if code != const.PRIVILEGE_TYPE_READ:
                    continue
            new_set = {}
            new_set["md_entity_id"] = id
            new_set["tenant_id"] = tenant_id
            str1 = code + ":" + str0
            new_set["privilege_code"] = str1[:100]
            new_set["privilege_type"] = code
            new_set["entity_type"] = entity_type
            new_set["ent_privilege_desc"] = str1[:600]

            entity_privilege_list.append(new_set)

    re = md.insert_execute(user_id, tenant_id, insert_entity_id, entity_privilege_list)
    logger.info('insert_entity_privilege,params={},insert result={}'.format(md_entity_ids, re))
    return re


def query_user_priv_by_user_account(user_account):
    user = ur.get_user(user_account)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    return query_user_privilege_by_userid(tenant_id, user_id)


def query_user_privilege_by_userid(tenant_id, user_id):
    sql = sql_query_privilege
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=(tenant_id, user_id,))
    result = cursor.fetchall()
    logger.info("query_user_privilege_by_userid,re:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


if __name__ == '__main__':
    user_account = "admin"
    user = ur.get_user(user_account)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    re = md.get_md_entities_by_code(tenant_id, ["entity_privileges"])
    if re is not None and len(re) > 0:
        insert_entity_id = re[0].get("md_entity_id")
    else:
        # entity_privileges实体表元数据实体ID
        insert_entity_id = 30029

    # #1.实体权限导入
    md_entity_ids = [30001, 300160]
    # re = insert_entity_privilege(user_id,tenant_id, insert_entity_id, ENTITY_TYPE_ENTITY, md_entity_ids)
    logger.info('result:{}'.format(re))

    # #2.视图权限写入
    view_ids = [50002]
    # re = insert_entity_privilege(user_id,tenant_id, insert_entity_id, ENTITY_TYPE_VIEW, view_ids)
    # logger.info('result:{}'.format(re))

    # re = query_user_priv_by_user_account(user_account)
    re = query_user_privilege_by_userid(tenant_id, user_id)
    logger.info('result:{}'.format(re))
