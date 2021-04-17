# #metadata_service.py
from flask import request, session, Response, g, jsonify
import json
from mdata import metadata as md, metadata_initialize as mdi, validate_rules as vr
from httpserver import httpserver
from config.config import cfg as config
from flask_httpauth import HTTPBasicAuth
from common import authorization as au
from service import utils_serv as utl

logger = config.logger
app = httpserver.getApp()
auth = HTTPBasicAuth()
domain_root = '/md'
GLOBAL_VIEW_ID = "$_VIEW_ID"


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
        logger.warning("[{}]用户账号或密码不正确，请确认并重试！".format(uname))
        return None
    vr = au.verify_password(uname, pwd, force=True)
    if not vr:
        logger.warning("用户账号=[{}]，用户登录失败，请输入正确的账号或密码！".format(uname))
        return None
    (token, expire_time) = au.generate_auth_token(g.user_id)
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
    logger.info("token:{}".format(token))
    return jsonify({'token': token, 'expire_time': expire_time})


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
    view_id = data.get(GLOBAL_VIEW_ID)
    if view_id is None:
        logger.warning('query View, param[$_VIEW_ID] should not be None')
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message='query View,$_VIEW_ID is None')
        return re
    if data is not None:
        for key in data.keys():
            if key == GLOBAL_VIEW_ID:
                data.pop(GLOBAL_VIEW_ID)
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
    re = None
    if (result is not None and len(result) > 0):
        ent_id = result[0].get('md_entity_id')
        (bool, re) = utl.query_privilege_check('findEntitySetup', ent_id, 'md_fields')
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
        (md_entity_id, public_flag, msg) = utl.getEntityIDByCode(tenant_id, md_entity_code, data)

    if md_entity_id is None:
        msg = None
        if md_entity_id is None and md_entity_code is None:
            msg = "queryEntityByCodeOrID, Input params [{}] or[{}] at least one should not none,please confirm.".format(
                utl.GLOBAL_ENTITY_ID, utl.GLOBAL_ENTITY_CODE)
        else:
            msg = "queryEntityByCodeOrID,the entity not found,input parma=(ID={},Code={})".format(md_entity_id,
                                                                                                  md_entity_code)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
    # 权限校验
    (bool, re) = utl.query_privilege_check('queryEntityByCodeOrID', md_entity_id, md_entity_code)
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


# 实体元数据对象属性信息查询,入参：{"$_ENTITY_ID":"123",$_ENTITY_CODE:"","only_active":Y/N}
@app.route(domain_root + '/services/queryFieldsByCodeOrID', methods=['POST', 'GET'])
@auth.login_required
def query_Metadata_Fields():
    data = utl.request_parse(request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    md_entity_code = data.get(utl.GLOBAL_ENTITY_CODE)
    only_active = data.get("only_active")
    b_onlyActive = True
    if only_active is not None and only_active == 'N':
        b_onlyActive = False
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    if md_entity_id is None and md_entity_code is not None:
        (md_entity_id, public_flag, msg) = utl.getEntityIDByCode(tenant_id, md_entity_code, data)
    if md_entity_id is None:
        msg = "queryFieldsByCodeOrID Input params [{}] or[{}] at least one should be none or not match,please checked.".format(
            utl.GLOBAL_ENTITY_ID,
            utl.GLOBAL_ENTITY_CODE)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
    # 权限校验
    (bool, re) = utl.query_privilege_check('queryFieldsByCodeOrID', md_entity_id, md_entity_code)
    if not bool:
        return Response(json.dumps(re), mimetype='application/json')
    res = md.get_md_fields(tenant_id, md_entity_id, b_onlyActive)
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
    # POST入参：{"$_ENTITY_ID":30025,"where":{"user_id":1348844049557229568}}
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
    # POST入参：{"$_ENTITY_CODE":"users","where":{"user_id":1348844049557229568}}
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
        res = md.get_md_entities_id_by_code([md_entity_code])
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


# Lookup条目查询by entity code
@app.route(domain_root + '/services/findLookupItemByCode', methods=['POST', 'GET'])
@auth.login_required
def find_lookupItem_by_code():
    # GET入参：{"lookup_code":"123"}
    # POST入参：{"lookup_code":['CODE1','CODE2']}
    data = utl.request_parse(request)
    data_list = []
    if request.method == 'POST':
        data_list = data.get('lookup_code')
    else:
        data_list.append(data.get('lookup_code'))
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    # user_id = user.get("user_id")
    res = md.get_md_entities_id_by_code(["lookup_classify"])
    md_entity_id = None
    if res is not None and len(res) > 0:
        md_entity_id = res[0].get("md_entity_id")
    else:
        s = 'findLookupItemByCode. Params:{},the Entity is not exists'.format(data_list)
        logger.warning(s)
        return md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                     message=s)
    res = md.get_lookup_items(tenant_id, data_list)
    sz = 0
    if (res is not None):
        sz = len(res)
    re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=sz, data=res,
                               message="query lookup success.")
    logger.info('findLookupItemByCode. Params:{},result:{}'.format(data_list, re))
    return Response(json.dumps(re), mimetype='application/json')


# 实体和Lookup mappig关系查询by entity code，lookup_classify
@app.route(domain_root + '/services/findLookupByEntityCode', methods=['POST', 'GET'])
@auth.login_required
def find_Lookup_By_EntityCode():
    # GET/POST入参：{"lookup_code":"123",entity_code:"xxx"}
    data = utl.request_parse(request)
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    lookup_code = data.get('lookup_code')
    entity_code = data.get('entity_code')
    if lookup_code == '':
        data.pop('lookup_code')
    if lookup_code is None or len(lookup_code.strip()) <= 0:
        lookup_code = entity_code
    res_lk = md.get_lookup_items(tenant_id, [lookup_code])
    res = md.get_md_entities_id_by_code([entity_code])
    md_entity_id = None
    if res is not None and len(res) > 0:
        md_entity_id = res[0].get("md_entity_id")
    else:
        s = 'findLookupByEntityCode. Params:{},the Entity is not exists'.format(data)
        logger.warning(s)
        return md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                     message=s)
    result = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_GET, "findLookupByEntityCode", data_list=None,
                                    where_list=[data])
    mp = utl.entity_lookup_mapping(res_lk, result.get("data"))
    size1 = 0
    if (mp is not None):
        size1 = len(mp)
    re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_SUCCESS, rows=size1, data=mp,
                               message="findLookupByEntityCode Success")
    logger.info('findLookupByEntityCode. Params:{},result:{}'.format(data, re))
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
        (md_entity_id, public_flag, msg) = utl.getEntityIDByCode(tenant_id, md_entity_code, data)
    if md_entity_id is None:
        msg = "queryEntityList ,md_entity_code not exists,please checked."
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
    # 权限校验
    (bool, re) = utl.query_privilege_check('queryEntityList', md_entity_id, md_entity_code)
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
    # 入参：{"$_ENTITY_ID":30001,"data":[{"test_fields":"Mark","test_fields1":"Mark0001"}]}
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
        data_list = []
        if data and data['data']:
            if isinstance(data['data'], list):
                data_list = data['data']
            else:
                data_list = [data['data']]
        data_list = utl.value2str(data_list)
        re = utl.sql_execute_method(md_entity_id, utl.SERVICE_METHOD_INSERT, "insertEntity", data_list=data_list)
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
    data_list = utl.value2str(data_list)
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
    # 入参：{"abc":"123"},必须要有主键ID参数
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


@app.route(domain_root + '/services/validateRules', methods=['POST', "GET"])
@auth.login_required
def run_rule_script():
    return rule_validate(request)


def rule_validate(http_request, insideInvoke=False):
    # 输入GET参数： {$_ENTITY_ID:123,rule_code:"xxxname",field_name:"xxxname",data:xxx}
    # 输入POST参数： {$_ENTITY_ID:123,rules:[{rule_code:1,field_name:"xxxname"},{rule_code:2,field_name:"xxxname1"}],n_roles:[],data:{rule_code:1,name:xxx}},
    # POST方式，rules=None，则校验所有规则，排除法就是n_rules={}。
    # output返回验证结果：
    # {
    #     "action": "VALIDATION",
    #     "status": 200,
    #     "rows": 1,
    #     "data": [
    #         {
    #             "rule_id": 6000003,
    #             "md_entity_id": 30015,
    #             "md_entity_code": "md_entities",
    #             "md_entity_name": "元数据实体",
    #             "md_entity_name_en": "md_entities"
    #             "rule_code": "rule_email",
    #             "rule_category": "Validation",
    #             "rule_type": "regex",
    #             "rule_name": "电子邮件(Email)",
    #             "rule_script": "\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*",
    #             "rule_desc": "电子邮件(Email)",
    #             "rule_desc_en": "",
    #             "input": "aMark@abc.com,www@ccc.com",#输入参数
    #             "output": "aMark@abc.com",#输出结果
    #             "result": true #验证通过与否
    #         }
    #     ],
    #     "message": "Validation Pass."
    # }
    if http_request is None:
        return
    data = utl.request_parse(http_request)
    md_entity_id = data.get(utl.GLOBAL_ENTITY_ID)
    rule_data = None
    rules = None
    n_rules = None
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    if http_request.method == 'GET':
        rules = []
        r_set = {}
        code = data.get("rule_code")
        if code is not None:
            r_set['rule_code'] = code
        f = data.get("field_name")
        if f is not None and len(f.strip()) > 0:
            r_set['field_name'] = f
        if r_set is not None and len(r_set) > 0:
            rules.append(r_set)
        d_set = {}
        if f is not None:
            d_set[f] = data.get("data")
        else:
            d_set = data.get("data")
        rule_data = d_set
    else:
        rules = data.get("rules")
        n_rules = data.get("n_rules")
        rule_data = data.get("data")
    rules_list = vr.get_rules(tenant_id, md_entity_id, rules, n_rules)
    size = 0
    if rules_list is not None:
        size = len(rules_list)
    is_pass, pass_list, not_pass_list = False, [], None
    if size == 0:
        logger.warning("get rules is nothing.input param:{}".format(data))
        is_pass = True
    else:
        (is_pass, pass_list, not_pass_list) = vr.validate_rules(rules_list, rule_data)
    message = "Validation Pass."
    iStatus = 200
    output_data = pass_list
    if not is_pass:
        message = "Validation not Pass."
        iStatus = 500
        output_data = not_pass_list

    if (insideInvoke):
        re = (is_pass, pass_list, not_pass_list)
        return re
    else:
        re = md.exec_output_status(type=md.DB_EXEC_TYPE_VALIDATE, status=iStatus, rows=size, data=output_data,
                                   message=message)
        return Response(json.dumps(re), mimetype='application/json')


if __name__ == '__main__':
    httpserver.startWebServer()
