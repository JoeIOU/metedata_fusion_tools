# #####utils_serv.py，Service服务相关的计算逻辑
import json
from flask import g
from mdata import metadata as md
from config.config import cfg as config
from common import constants as const, cache
from privilege import role_privilege as rp
from mdata import index_unique as idx
from data import data_view as vw

HTTP_STATUS_CODE_NOT_RIGHT = 401
HTTP_STATUS_CODE_FORBIDDEN = 403

SERVICE_METHOD_INSERT = "Insert"
SERVICE_METHOD_UPDATE = "Update"
SERVICE_METHOD_DELETE = "Delete"
SERVICE_METHOD_GET = "Query"
SERVICE_METHOD_VIEW = "ViewQuery"
# 全局实体元数据ID。
GLOBAL_ENTITY_ID = "$_ENTITY_ID"
GLOBAL_ENTITY_CODE = "$_ENTITY_CODE"

logger = config.logger


def request_parse(req):
    d = None
    data = None
    # '''解析请求数据并以json形式返回'''
    if req.method == 'POST':
        if req.is_json:
            data = req.json
        else:
            fm = req.form
            if fm is not None:
                data = fm.to_dict()
    elif req.method == 'GET':
        data = req.args
    if data is not None and not isinstance(data, dict):
        d = json.loads(json.dumps(data))
    else:
        d = data
    return d


def get_login_user():
    user_id = g.user_id
    user = None
    if user_id is not None:
        user = cache.get(user_id)
    if user is None:
        cache.remove(user_id + '_privilege')
        logger.warning("the user does not login,please login first.")
    return user


def get_login_user_privilege():
    user_id = g.user_id
    user = None
    if user_id is not None:
        user = cache.get(user_id)
    user_privilege_list = cache.get(user_id + '_privilege')
    if user is None:
        cache.remove(user_id + '_privilege')
        logger.warning("the user does not login,please login first.")
        return None
    tenant_id = user.get("tenant_id")
    user_id1 = user.get("user_id")
    if user_privilege_list is None:
        user_privilege_list = rp.query_user_privilege_by_userid(tenant_id, user_id1)
        cache.push(user_id + '_privilege', user_privilege_list)
    return user_privilege_list


def remove_privilege():
    user_id = g.user_id
    cache.remove(user_id + '_privilege')
    cache.remove(user_id)
    return True


def have_privilege(md_entity_id, method):
    user_id = g.user_id
    user_privilege_list = cache.get(user_id + '_privilege')
    b_privilege = False
    if user_privilege_list is None:
        msg = 'you does not have any privilege ,please login again,or ask the service center for help.'
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None, message=msg)
        logger.warning(output)
        return b_privilege
    if isinstance(md_entity_id, str):
        i_md_entity_id = int(md_entity_id)
    else:
        i_md_entity_id = md_entity_id
    for item in user_privilege_list:
        privllege_entity_id = item.get("md_entity_id")
        privilege_type = item.get("privilege_type")
        if privllege_entity_id == i_md_entity_id:
            if method == SERVICE_METHOD_GET:
                if privilege_type == const.PRIVILEGE_TYPE_READ:
                    b_privilege = True
                    break
            elif method == SERVICE_METHOD_INSERT:
                if (privilege_type == const.PRIVILEGE_TYPE_CREATE):
                    b_privilege = True
                    break
            elif method == SERVICE_METHOD_UPDATE:
                if (privilege_type == const.PRIVILEGE_TYPE_UPDATE):
                    b_privilege = True
                    break
            elif method == SERVICE_METHOD_DELETE:
                if (privilege_type == const.PRIVILEGE_TYPE_DELETE):
                    b_privilege = True
                    break
            else:
                continue
    return b_privilege


def get_index_data_ids(data):
    ids = None
    if data is not None:
        d = data.get("data")
        if d is not None and d.get("ids") is not None:
            ids = d.get("ids")
    return ids


def sql_execute_method(md_entity_id, method, service_name, data_list=None, where_list=None):
    user_id = g.user_id
    user_privilege_list = cache.get(user_id + '_privilege')
    user = cache.get(user_id)
    if user is None:
        msg = 'access service, user does not login ,please login first.'
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_FORBIDDEN, rows=0, data=None, message=msg)
        return output
    if user_privilege_list is None or len(user_privilege_list) == 0:
        msg = 'access service, user({}) does not have privilege,entity=[{}] ,please login again.'.format(
            user.get("account_number"), md_entity_id)
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None, message=msg)
        return output
    b_privilege = have_privilege(md_entity_id, method)
    if not b_privilege:
        msg = '{},you do not have the privilege to access the service[{}],entity=[{}],please check and confirm,any question please ask the service center for help,thanks.'.format(
            user.get("account_number"), service_name, md_entity_id)
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None, message=msg)
        return output

    user_id = None
    tenant_id = None
    if user is not None:
        user_id = user.get("user_id")
        tenant_id = user.get("tenant_id")
    re = None
    try:
        if method == SERVICE_METHOD_GET:
            re = md.query_execute(user_id, tenant_id, md_entity_id, where_list[0])
        elif method == SERVICE_METHOD_INSERT:
            re = md.insert_execute(user_id, tenant_id, md_entity_id, data_list)
            # 插入索引数据
            if re is not None:
                iRows = re.get("rows")
                if iRows is not None and iRows > 0:
                    ids = get_index_data_ids(re)
                    ids_list = ids2_where(ids)
                    try:
                        idx.insert_index_data(user_id, tenant_id, md_entity_id, data_list, ids)
                    except Exception as ex:
                        # 插入有异常，如唯一键重复等，则删除回滚。
                        re = md.delete_execute(user_id, tenant_id, md_entity_id, ids_list)
                        idx.delete_index_data(user_id, tenant_id, md_entity_id, where_list, ids)
                        raise ex
        elif method == SERVICE_METHOD_DELETE:
            re = md.delete_execute(user_id, tenant_id, md_entity_id, where_list)
            # 删除索引数据
            if re is not None:
                iRows = re.get("rows")
                if iRows is not None and iRows > 0:
                    ids = get_index_data_ids(re)
                    idx.delete_index_data(user_id, tenant_id, md_entity_id, where_list, ids)
        elif method == SERVICE_METHOD_UPDATE:
            re = md.update_execute(user_id, tenant_id, md_entity_id, data_list, where_list)
            # 更新索引数据
            if re is not None:
                iRows = re.get("rows")
                if iRows is not None and iRows > 0:
                    ids = get_index_data_ids(re)
                    idx.update_index_data(user_id, tenant_id, md_entity_id, data_list, ids)
        elif method == SERVICE_METHOD_VIEW:
            re = vw.query_view(user_id, md_entity_id, where_list[0])
        else:
            re = md.query_execute(user_id, tenant_id, md_entity_id, where_list[0])
        return re
    except Exception as e:
        msg = 'execute method error,message:%s' % (e)
        logger.error(msg)
        output = md.exec_output_status(type=method, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None, message=msg)
        return output


def ids2_where(ids):
    if ids is None:
        return None
    id_list = []
    for id in ids:
        d = {}
        d[md.KEY_FIELDS_ID] = id
        id_list.append(d)
    return id_list
