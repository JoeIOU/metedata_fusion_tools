# #metadata_service.py
from flask import request, session, Response
import json
from mdata import metadata as md,metadata_initialize as mdi
from privilege import role_privilege as rp, user_mngt as ur
from mdata import index_unique as idx
from data import data_view as vw
from httpserver import httpserver
from config.config import cfg as config
from common import constants as const

# from db.db_conn import db_connection_metedata as db_md

logger = config.logger
domain_root = '/md'

app = httpserver.getApp()
HTTP_STATUS_CODE_NOT_RIGHT = 401
HTTP_STATUS_CODE_FORBIDDEN = 403

SERVICE_METHOD_INSERT = "Insert"
SERVICE_METHOD_UPDATE = "Update"
SERVICE_METHOD_DELETE = "Delete"
SERVICE_METHOD_GET = "Query"
SERVICE_METHOD_VIEW = "ViewQuery"
user_privilege_list = None
# 全局实体元数据ID。
GLOBAL_ENTITY_ID = "$_ENTITY_ID"
GLOBAL_ENTITY_CODE = "$_ENTITY_CODE"


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


@app.route(domain_root + '/env_profile', methods=['GET'])
def env_profile():
    return config.ENV


def login_verify(user_account, password):
    if user_account is None or password is None:
        return None
    login_flag = False
    # -------------
    # verify code...
    # --------------

    # if login_flag:
    if True:
        re = ur.get_user(user_account)
        logger.info("login success,user info:{}".format(re))
    return re


# test url= http://127.0.0.1:8888/md/login?user_account=test1&user_name=Joe.Lin
@app.route(domain_root + "/login", methods=['GET'])
def login():
    data = request_parse(request)
    """设置session的数据"""
    user_acc = data.get('user_account')
    pwd = data.get('password')
    if pwd is None:
        pwd = ''
    if user_acc is None:
        logger.warning("user account is NULL.")
        return None
    re = login_verify(user_acc, pwd)
    out_data = None
    if re is None:
        logger.warning("user account[{}] is not exists.".format(user_acc))
    else:
        session["user_account"] = user_acc
        session["user_name"] = data.get('user_name')
        session["user"] = re
        logger.warning("user:[{}] login success.".format(user_acc))
        msg = "success"
        out_data = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=md.DB_EXEC_STATUS_SUCCESS, rows=0,
                                         data=data, message=msg)
    return Response(json.dumps(out_data), mimetype='application/json')


@app.route(domain_root + "/logout", methods=['GET'])
def logout():
    user_acc = session["user_account"]
    """设置session的数据"""
    session["user_account"] = None
    session["user_name"] = None
    logger.warning("user:[{}] logout success.".format(user_acc))
    msg = "logout success!"
    global user_privilege_list
    user_privilege_list = None
    out_data = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=md.DB_EXEC_STATUS_SUCCESS, rows=0,
                                     data=user_acc, message=msg)
    return Response(json.dumps(out_data), mimetype='application/json')


def get_login_user():
    global user_privilege_list
    user = None
    if session is not None:
        user = session.get("user")
        if user is None:
            user_privilege_list = None
            logger.warning("the user does not login,please login first.")
        else:
            tenant_id = user.get("tenant_id")
            user_id = user.get("user_id")
            user_privilege_list = rp.query_user_privilege_by_userid(tenant_id, user_id)
    return user


@app.route(domain_root + '/user', methods=['GET'])
def get_userinfo():
    re = get_login_user()
    msg = "success"
    if re is None:
        msg = "there is no one login,please login first."
        re = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status="401", rows=0,
                                   data=None, message=msg)
    else:
        re = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=md.DB_EXEC_STATUS_SUCCESS, rows=1,
                                   data=re, message=msg)
    return Response(json.dumps(re), mimetype='application/json')


def have_privilege(md_entity_id, method):
    b_privilege = False
    global user_privilege_list
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
            elif method == SERVICE_METHOD_INSERT or method == SERVICE_METHOD_UPDATE:
                if (privilege_type == const.PRIVILEGE_TYPE_UPDATE or privilege_type == const.PRIVILEGE_TYPE_CREATE):
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


def sql_execute_method(md_entity_id, method, data_list=None, where_list=None):
    user = get_login_user()
    if user is None:
        msg = 'access service, user does not login ,please login first.'
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_FORBIDDEN, rows=0, data=None, message=msg)
        return output
    global user_privilege_list
    if user_privilege_list is None or len(user_privilege_list) == 0:
        msg = 'access service, user({}) does not have privilege,entity=[{}] ,please login again.'.format(
            user.get("account_number"), md_entity_id)
        logger.warning(msg)
        output = md.exec_output_status(type=method, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None, message=msg)
        return output
    b_privilege = have_privilege(md_entity_id, method)
    if not b_privilege:
        msg = '{},you do not have the privilege to access the service,entity=[{}],please check and confirm,any question please ask the service center for help,thanks.'.format(
            user.get("account_number"), md_entity_id)
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


# 视图查询
@app.route(domain_root + '/services/queryView', methods=['POST', 'GET'])
def query_view():
    data = request_parse(request)
    view_id = data.get("view_id")
    if view_id is None:
        logger.warning('query View, view_id should not be None')
        return '{view_id is None}'
    if data is not None:
        for key in data.keys():
            if key == "view_id":
                data.pop("view_id")
                break
    re = sql_execute_method(view_id, SERVICE_METHOD_VIEW, data_list=None, where_list=[data])

    logger.info('view result:{}'.format(re))
    return Response(json.dumps(re), mimetype='application/json')

# 实体元数据对象配置信息查询
@app.route(domain_root + '/services/findEntitySetup', methods=['POST', 'GET'])
def find_entity_setup():
    global user_privilege_list
    # 入参：{"abc":"123"}
    data = request_parse(request)
    md_entity_id = data.get(GLOBAL_ENTITY_ID)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'findEntitySetup,input entity params[{}] should not be None.'.format(GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        user = get_login_user()
        tenant_id = user.get("tenant_id")
        if user_privilege_list is None or len(user_privilege_list) == 0:
            msg = 'access findEntitySetup service, user({}) does not have privilege,entity=[{}] ,please login again.'.format(
                user.get("account_number"), md_entity_id)
            logger.warning(msg)
            output = md.exec_output_status(type=SERVICE_METHOD_GET, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None,
                                           message=msg)
            return output
        b_privilege = have_privilege(md_entity_id, SERVICE_METHOD_GET)
        if not b_privilege:
            msg = '{},you do not have the privilege to access the find_entity_setup service,entity=[{}],please check and confirm,any question please ask the service center for help,thanks.'.format(
                user.get("account_number"), md_entity_id)
            logger.warning(msg)
            output = md.exec_output_status(type=SERVICE_METHOD_GET, status=HTTP_STATUS_CODE_NOT_RIGHT, rows=0, data=None,
                                           message=msg)
            return output
        res=mdi.query_entity_fields_columns(tenant_id,md_entity_id)
        irows=0
        if res is not None:
            irows=len(res)
        re = md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=irows, data=res,
                            message='query Entity Setup Info Success.')
        logger.info('find Entity Setup. Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')

# 实体详情查询
@app.route(domain_root + '/services/findEntity', methods=['POST', 'GET'])
def find_entity():
    # 入参：{"abc":"123"}
    data = request_parse(request)
    md_entity_id = data.get(GLOBAL_ENTITY_ID)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'findEntity,input entity params[{}] should not be None.'.format(GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = sql_execute_method(md_entity_id, SERVICE_METHOD_GET, data_list=None, where_list=[data])
        logger.info('find Entity. Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体详情查询by entity code
@app.route(domain_root + '/services/findEntityByCode', methods=['POST', 'GET'])
def find_entity_by_code():
    # 入参：{"abc":"123"}
    data = request_parse(request)
    md_entity_code = data.get(GLOBAL_ENTITY_CODE)
    if md_entity_code is None or len(md_entity_code) <= 0:
        msg = 'findEntityByCode,input entity code params[{}] should not be None.'.format(GLOBAL_ENTITY_CODE)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        user = get_login_user()
        tenant_id = user.get("tenant_id")
        # user_id = user.get("user_id")
        res = md.get_md_entities_by_code(tenant_id, [md_entity_code])
        md_entity_id = None
        if res is not None and len(res) > 0:
            md_entity_id = res[0].get("md_entity_id")
        else:
            s = 'findEntityByCode. Params:{},the Entity is not exists'.format(data)
            logger.warning(s)
            return md.exec_output_status(type=SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                         message=s)
        re = sql_execute_method(md_entity_id, SERVICE_METHOD_GET, data_list=None, where_list=[data])
        logger.info('findEntityByCode. Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体插入Insert
@app.route(domain_root + '/services/insertEntity', methods=['POST'])
def insert_entity():
    # 入参：{"abc":"123"}
    data = request_parse(request)
    if data is None:
        msg = 'insert Entity, input param[{}] should not be None.'.format(GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_INSERT, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return json.dumps(re)

    md_entity_id = data.get(GLOBAL_ENTITY_ID)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'insert Entity, input param[{}] should not be None.'.format(GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_INSERT, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = sql_execute_method(md_entity_id, SERVICE_METHOD_INSERT, data_list=[data])
        logger.info('insert Entity Params:%s' % data)
    return Response(json.dumps(re), mimetype='application/json')


# 单个实体更新，通过request.args输入单个对象的id，name等参数,body输入更新的信息
@app.route(domain_root + '/services/updateEntity', methods=['POST'])
def update_entity():
    # 入参：{"abc":"123"}
    data = request_parse(request)
    wh_dict = request.args
    if wh_dict is not None:
        wh_dict = json.loads(json.dumps(wh_dict))
    wh_list = []
    wh_list.append(wh_dict)
    md_entity_id = data.get(GLOBAL_ENTITY_ID)
    ls_data = []
    if isinstance(data, list):
        ls_data = data
    else:
        ls_data.append(data)
    re = update_entity_common(md_entity_id, ls_data, wh_list)
    return Response(json.dumps(re), mimetype='application/json')


# 批量实体更新，通过where和data list两个json 数据输入格式：{md_entity_id:12345,data:[{},{}],where:[{},{}]}
@app.route(domain_root + '/services/updateEntityBatch', methods=['POST'])
def update_entity_batch():
    # 入参：{"abc":"123"}
    data = request_parse(request)
    if data is None:
        msg = 'update Entity Batch, input params should not be None.'
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_UPDATE, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return re

    md_entity_id = data.get(GLOBAL_ENTITY_ID)
    where_list = data.get("where")
    data_list = data.get("data")
    re = update_entity_common(md_entity_id, data_list, where_list)
    return Response(json.dumps(re), mimetype='application/json')


# 更新数据的方法，支持单个或多个对象更新，要求同一个实体的。
def update_entity_common(md_entity_id, data_list, where_list):
    if md_entity_id is None:
        msg = 'update Entity, input param[{}] should not be None.'.format(GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_UPDATE, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = sql_execute_method(md_entity_id, SERVICE_METHOD_UPDATE, data_list=data_list, where_list=where_list)
        logger.info('update Entity Params:{}'.format(data_list))
    return re


# 删除数据
@app.route(domain_root + '/services/deleteEntity', methods=['POST'])
def delete_entity():
    # 入参：{"abc":"123"}
    wh_dict = request_parse(request)
    if wh_dict is not None:
        wh_dict = json.loads(json.dumps(wh_dict))
    wh_list = []
    if isinstance(wh_dict, list):
        wh_list = wh_dict
    else:
        wh_list.append(wh_dict)
    md_entity_id = wh_dict.get(GLOBAL_ENTITY_ID)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'delete Entity, input param[{}] should not be None.'.format(GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=SERVICE_METHOD_DELETE, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = sql_execute_method(md_entity_id, SERVICE_METHOD_DELETE, data_list=None, where_list=wh_list)
        logger.info('delete Entity Params:{}'.format(wh_list))
    return Response(json.dumps(re), mimetype='application/json')


if __name__ == '__main__':
    httpserver.startWebServer()
