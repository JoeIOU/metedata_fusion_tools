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
    if data is not None:
        d = json.loads(json.dumps(data))
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


def get_login_user_privilege(force=False):
    user_id = g.user_id
    user = None
    if user_id is not None:
        user = cache.get(user_id)
    else:
        logger.warning("the user does not login,please login first.")
        return None
    user_privilege_list = cache.get(user_id + '_privilege')
    if user is None:
        cache.remove(user_id + '_privilege')
        logger.warning("the user does not login,please login first.")
        return None
    tenant_id = user.get("tenant_id")
    user_id1 = user.get("user_id")
    if user_privilege_list is None or force:
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
    for item in user_privilege_list:
        privllege_entity_id = item.get("md_entity_id")
        privilege_type = item.get("privilege_type")
        if str(privllege_entity_id) == str(md_entity_id):
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
        msg = '{}，您访问服务{}受阻,用户未登录或登录过期，请重新登录。'.format(user_id,service_name)
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_FORBIDDEN, rows=0, data=None, message=msg)
        return output
    if user_privilege_list is None or len(user_privilege_list) == 0:
        msg = '{}，您无权访问服务{}受阻，实体ID=[{}]，请申请权限或找业务管理员寻求帮忙，谢谢。'.format(user.get("account_number"),service_name,
             md_entity_id)
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None, message=msg)
        return output
    b_privilege = have_privilege(md_entity_id, method)
    if not b_privilege:
        msg = '{}，您无权访问这个实体（实体ID={}）的这个服务[{}],请申请权限或找业务管理员寻求帮忙，谢谢。'.format(
            user.get("account_number"), md_entity_id, service_name)
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
            wh_dict = None
            if where_list is not None:
                if isinstance(where_list, list) and len(where_list) > 0:
                    wh_dict = where_list[0]
                elif isinstance(where_list, dict):
                    wh_dict = where_list
            re = md.query_execute(user_id, tenant_id, md_entity_id, wh_dict)
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


def query_privilege_check(method_name, md_entity_id, entity_code):
    if md_entity_id is not None and not isinstance(md_entity_id, str):
        md_entity_id = str(md_entity_id)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = '[Privilege Validation]:Access Service={},entity=[{}] should not be None.'.format(method_name, GLOBAL_ENTITY_ID)
        logger.warning(msg)
        output = md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                       message=msg)
        return (False, output)
    else:
        user = get_login_user()
        user_privilege_list = get_login_user_privilege()
        if user_privilege_list is None or len(user_privilege_list) == 0:
            msg = '{}，您无权访问服务{}(实体ID={},实体编码={})，请申请权限或找业务管理员帮忙。'.format(
                 user.get("account_number"),method_name, md_entity_id, entity_code)
            logger.warning(msg)
            output = md.exec_output_status(type=SERVICE_METHOD_GET, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0,
                                           data=None,
                                           message=msg)
            return (False, output)
        b_privilege = have_privilege(md_entity_id, SERVICE_METHOD_GET)
        if not b_privilege:
            msg = '{}，您无权访问服务{}(实体ID={},实体编码={})，请申请权限或找业务管理员帮忙。'.format(
                user.get("account_number"), method_name, md_entity_id, entity_code)
            logger.warning(msg)
            output = md.exec_output_status(type=SERVICE_METHOD_GET, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0,
                                           data=None,
                                           message=msg)
            return (False, output)
    return (True, None)


def getEntityIDByCode(tenant_id, md_entity_code, data):
    res = md.get_md_entities_id_by_code([md_entity_code])
    md_entity_id = None
    msg = None
    if res is not None and len(res) > 0:
        md_entity_id = res[0].get("md_entity_id")
    else:
        s = 'findEntityByCode. Params:{},the Entity is not exists'.format(data)
        logger.warning(s)
        msg = md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                    message=s)
    return (md_entity_id, msg)
