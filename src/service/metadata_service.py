# #metadata_service.py
from flask import request, session, Response, g, jsonify
import json
from mdata import metadata as md, metadata_initialize as mdi
from httpserver import httpserver
from config.config import cfg as config
from flask_httpauth import HTTPBasicAuth
from common import authorization as au
from service import utils_serv as utl

logger = config.logger
app = httpserver.getApp()
auth = HTTPBasicAuth()
domain_root = '/md'


@app.route("/", methods=["GET"])
def get_index():
    return app.send_static_file('index.html')


# 验证token
@auth.verify_password
def verify_password(username, password):
    bool = au.verify_password(username, password)
    if bool:
        utl.get_login_user_privilege()
    return bool


@app.route(domain_root + '/env_profile', methods=['GET'])
@auth.login_required
def env_profile():
    return config.ENV


# test url= http://127.0.0.1:8888/md/login?username=test1&password=112233
@app.route(domain_root + "/login", methods=['GET', 'POST'])
# @auth.login_required
def login():
    data = utl.request_parse(request)
    """设置session的数据"""
    uname = data.get('username')
    pwd = data.get('password')
    if uname is None or len(uname.strip()) <= 0 or pwd is None or len(pwd.strip()) <= 0:
        logger.warning("user account[{}] or password is NULL,please input again".format(uname))
        return None
    vr = au.verify_password(uname, pwd, force=True)
    if not vr:
        logger.warning("user account[{}] login failed,please input the right username and password.".format(uname))
        return None
    token = au.generate_auth_token(g.user_id)
    re = g.user
    if re is None:
        logger.warning("user account is not exists.")
    else:
        session["user_account"] = re.get('account_number')
        session["user_name"] = re.get('user_name')
        session["user"] = re
        logger.warning("user:[{}] login success.".format(re.get('account_number')))
        # 获取权限
        utl.get_login_user_privilege(force=True)
        # msg = "login success."
        # out_data = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=md.DB_EXEC_STATUS_SUCCESS, rows=0,
        #                                  data=re, message=msg)
        # return Response(json.dumps(out_data), mimetype='application/json')
    logger.info("token:{}".format(token))
    return jsonify({'token': token})


@app.route(domain_root + "/logout", methods=['GET', 'POST'])
@auth.login_required
def logout():
    user_acc = session["user_account"]
    """设置session的数据"""
    session["user_account"] = None
    session["user_name"] = None
    session["user"] = None
    g.user = None
    logger.warning("user:[{}] logout success.".format(user_acc))
    msg = "logout success!"
    utl.remove_privilege()
    g.user_id = None
    out_data = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=md.DB_EXEC_STATUS_SUCCESS, rows=0,
                                     data=user_acc, message=msg)
    return Response(json.dumps(out_data), mimetype='application/json')


@app.route(domain_root + '/services/user', methods=['GET'])
@auth.login_required
def get_userinfo():
    re = utl.get_login_user()
    msg = "success"
    if re is None:
        msg = "there is no one login,please login first."
        re = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status="401", rows=0,
                                   data=None, message=msg)
    else:
        re = md.exec_output_status(type=md.DB_EXEC_TYPE_QUERY, status=md.DB_EXEC_STATUS_SUCCESS, rows=1,
                                   data=re, message=msg)
    return Response(json.dumps(re), mimetype='application/json')


# 视图查询
@app.route(domain_root + '/services/queryView', methods=['POST', 'GET'])
@auth.login_required
def query_view():
    data = utl.request_parse(request)
    view_id = data.get("view_id")
    if view_id is None:
        logger.warning('query View, view_id should not be None')
        return '{view_id is None}'
    if data is not None:
        for key in data.keys():
            if key == "view_id":
                data.pop("view_id")
                break
    re = utl.sql_execute_method(view_id, utl.SERVICE_METHOD_VIEW, "queryView", data_list=None, where_list=[data])

    logger.info('view result:{}'.format(re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体元数据对象配置信息查询
@app.route(domain_root + '/services/findEntitySetup', methods=['POST', 'GET'])
@auth.login_required
def find_entity_setup():
    # 入参：{"abc":"123"}
    data = utl.request_parse(request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    bool = False
    result = md.get_md_entities_id_by_code(['md_fields'])
    if (result is not None and len(result) > 0):
        ent_id = result[0].get('md_entity_id')
        (bool, re) = utl.query_privilege_check('findEntitySetup', ent_id)
    if not bool:
        return Response(json.dumps(re), mimetype='application/json')
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    res = mdi.query_entity_fields_columns(tenant_id, md_entity_id)
    irows = 0
    if res is not None:
        irows = len(res)
    re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=irows, data=res,
                               message='query Entity Setup Info Success.')
    logger.info('find Entity Setup. Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体元数据对象信息查询,入参：{"$_ENTITY_ID":"123",$_ENTITY_CODE:""}
@app.route(domain_root + '/services/queryEntityByCodeOrID', methods=['POST', 'GET'])
@auth.login_required
def query_Metadata_Entity():
    data = utl.request_parse(request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    md_entity_code = data.get(utl.GLOBAL_ENTITY_CODE)
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    if md_entity_id is None and md_entity_code is not None:
        (md_entity_id, msg) = utl.getEntityIDByCode(tenant_id, md_entity_code, data)

    if md_entity_id is None:
        msg = "queryEntityByCodeOrID Input params [{}] or[{}] at least one should be none or not match,please checked.".format(
            utl.GLOBAL_ENTITY_ID,
            utl.GLOBAL_ENTITY_CODE)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
    # 权限校验
    (bool, re) = utl.query_privilege_check('queryEntityByCodeOrID', md_entity_id)
    if not bool:
        return Response(json.dumps(re), mimetype='application/json')
    res = md.get_md_entities(tenant_id, [md_entity_id])
    irows = 0
    if res is not None:
        irows = len(res)
    re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=irows, data=res,
                               message='queryEntityByCodeOrID Info Success.')
    logger.info('queryEntityByCodeOrID, Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体元数据对象属性信息查询,入参：{"$_ENTITY_ID":"123",$_ENTITY_CODE:""}
@app.route(domain_root + '/services/queryFieldsByCodeOrID', methods=['POST', 'GET'])
@auth.login_required
def query_Metadata_Fields():
    data = utl.request_parse(request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    md_entity_code = data.get(utl.GLOBAL_ENTITY_CODE)
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    if md_entity_id is None and md_entity_code is not None:
        (md_entity_id, msg) = utl.getEntityIDByCode(tenant_id, md_entity_code, data)
    if md_entity_id is None:
        msg = "queryFieldsByCodeOrID Input params [{}] or[{}] at least one should be none or not match,please checked.".format(
            utl.GLOBAL_ENTITY_ID,
            utl.GLOBAL_ENTITY_CODE)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
    # 权限校验
    (bool, re) = utl.query_privilege_check('queryFieldsByCodeOrID', md_entity_id)
    if not bool:
        return Response(json.dumps(re), mimetype='application/json')
    res = md.get_md_fields(tenant_id, md_entity_id)
    irows = 0
    if res is not None:
        irows = len(res)
    re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=irows, data=res,
                               message='queryFieldsByCodeOrID Info Success.')
    logger.info('queryFieldsByCodeOrID, Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体详情查询
@app.route(domain_root + '/services/findEntity', methods=['POST', 'GET'])
@auth.login_required
def find_entity():
    # GET入参：{"$_ENTITY_ID":30025,"user_id":"123"}
    # POST入参：{"$_ENTITY_ID":30025,"where":[{"user_id":1348844049557229568},{"user_id":1348892817107324928}]}
    data_list = []
    data = utl.request_parse(request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    if not isinstance(md_entity_id, str):
        md_entity_id = str(md_entity_id)
    if request.method == 'POST':
        data_list = data.get('where')
    else:
        data_list.append(data)

    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'findEntity,input entity params[{}] should not be None.'.format(utl.GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_GET, "findEntity", data_list=None,
                                    where_list=data_list)
        logger.info('find Entity. Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体详情查询by entity code
@app.route(domain_root + '/services/findEntityByCode', methods=['POST', 'GET'])
@auth.login_required
def find_entity_by_code():
    # GET入参：{"$_ENTITY_CODE":"users","user_id":"123"}
    # POST入参：{"$_ENTITY_CODE":"users","where":[{"user_id":1348844049557229568},{"user_id":1348892817107324928}]}
    data = utl.request_parse(request)
    data_list = []
    if request.method == 'POST':
        data_list = data.get('where')
    else:
        data_list.append(data)
    md_entity_code = data.get(utl.GLOBAL_ENTITY_CODE)
    if md_entity_code is None or len(md_entity_code) <= 0:
        msg = 'findEntityByCode,input entity code params[{}] should not be None.'.format(utl.GLOBAL_ENTITY_CODE)
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        user = utl.get_login_user()
        tenant_id = user.get("tenant_id")
        # user_id = user.get("user_id")
        res = md.get_md_entities_by_code(tenant_id, [md_entity_code])
        md_entity_id = None
        if res is not None and len(res) > 0:
            md_entity_id = res[0].get("md_entity_id")
        else:
            s = 'findEntityByCode. Params:{},the Entity is not exists'.format(data_list)
            logger.warning(s)
            return md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                         message=s)
        re = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_GET, "findEntityByCode", data_list=None,
                                    where_list=data_list)
        logger.info('findEntityByCode. Params:{},result:{}'.format(data_list, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体表查询by table name list
@app.route(domain_root + '/services/findTableByName', methods=['POST', 'GET'])
@auth.login_required
def find_table_by_name():
    # POST入参：{"table_names":["abc","123"]} or GET入参 {table_names=abc}
    data = utl.request_parse(request)
    tableName = data.get("table_names")
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    # user_id = user.get("user_id")
    name_list = []
    if tableName is not None and isinstance(tableName, list):
        name_list = tableName
    elif tableName is not None:
        name_list.append(tableName)
    else:
        name_list = None

    res = md.get_md_tables_by_name(tenant_id, name_list)
    out = None
    if res is not None and len(res) > 0:
        s = 'findTableByName success'.format(data)
        logger.info(s)
        icount = len(res)
        out = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=icount,
                                    data=res, message=s)
    else:
        s = 'findTableByName. Params:{},the Entity is not exists'.format(data)
        logger.warning(s)
        out = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                    message=s)
    logger.info('findTableByName. Params:{},result:{}'.format(data, res))
    return Response(json.dumps(out), mimetype='application/json')


# 实体元数据对象清单查询,入参：{}
@app.route(domain_root + '/services/queryEntityList', methods=['POST', 'GET'])
@auth.login_required
def query_entity_list():
    data = utl.request_parse(request)
    md_entity_id = None
    md_entity_code = "md_entities"
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    if md_entity_id is None and md_entity_code is not None:
        (md_entity_id, msg) = utl.getEntityIDByCode(tenant_id, md_entity_code, data)
    if md_entity_id is None:
        msg = "queryEntityList ,md_entity_code not exists,please checked."
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
    # 权限校验
    (bool, re) = utl.query_privilege_check('queryEntityList', md_entity_id)
    if not bool:
        return Response(json.dumps(re), mimetype='application/json')
    res = md.get_md_entities_list(tenant_id)
    irows = 0
    if res is not None:
        irows = len(res)
    re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=irows, data=res,
                               message='queryEntityList Info Success.')
    logger.info('queryEntityList, Params:{},result:{}'.format(data, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体插入Insert
@app.route(domain_root + '/services/insertEntity', methods=['POST'])
@auth.login_required
def insert_entity():
    # 入参：{"abc":"123"}
    data = utl.request_parse(request)
    if data is None:
        msg = 'insert Entity, input param[{}] should not be None.'.format(utl.GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_INSERT, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return json.dumps(re)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    if not isinstance(md_entity_id, str):
        md_entity_id = str(md_entity_id)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'insert Entity, input param[{}] should not be None.'.format(utl.GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_INSERT, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        list_data = []
        if data and data['data']:
            if isinstance(data['data'], list):
                list_data = data['data']
            else:
                list_data = [data['data']]
        re = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_INSERT, "insertEntity", data_list=list_data)
        logger.info('insert Entity Params:%s' % data)
    return Response(json.dumps(re), mimetype='application/json')


# 单个或多个实体更新，入参：{"$_ENTITY_ID":30025,"data":[{"user_name":"test01"},{"user_name":"test02"}],"where":[{"user_id":1348844049557229568},{"user_id":1348892817107324928}]}
@app.route(domain_root + '/services/updateEntity', methods=['POST'])
@auth.login_required
def update_entity():
    # 入参：{"$_ENTITY_ID":30025,"data":[{"user_name":"test01"},{"user_name":"test02"}],"where":[{"user_id":1348844049557229568},{"user_id":1348892817107324928}]}
    data = utl.request_parse(request)
    if data is None:
        msg = 'updateEntity, input params should not be None.'
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_UPDATE, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return re

    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    where_list = data.get("where")
    data_list = data.get("data")
    re = update_entity_common(md_entity_id, data_list, where_list)
    return Response(json.dumps(re), mimetype='application/json')


# 更新数据的方法，支持单个或多个对象更新，要求同一个实体的。
def update_entity_common(md_entity_id, data_list, where_list):
    if md_entity_id is None:
        msg = 'update Entity, input param[{}] should not be None.'.format(utl.GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_UPDATE, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_UPDATE, "updateEntity", data_list=data_list,
                                    where_list=where_list)
        logger.info('update Entity Params:{}'.format(data_list))
    return re


# 删除数据
@app.route(domain_root + '/services/deleteEntity', methods=['POST'])
@auth.login_required
def delete_entity():
    # 入参：{"abc":"123"}
    data = utl.request_parse(request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    where_list = data.get("where")
    if md_entity_id is not None and not isinstance(md_entity_id, str):
        md_entity_id = str(md_entity_id)
    if md_entity_id is None or len(md_entity_id) <= 0:
        msg = 'delete Entity, input param[{}] should not be None.'.format(utl.GLOBAL_ENTITY_ID)
        logger.warning(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_DELETE, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
    else:
        re = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_DELETE, "deleteEntity", data_list=None,
                                    where_list=where_list)
        logger.info('delete Entity Params:{}'.format(where_list))
    return Response(json.dumps(re), mimetype='application/json')


if __name__ == '__main__':
    httpserver.startWebServer()
