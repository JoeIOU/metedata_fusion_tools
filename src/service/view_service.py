# #view_service.py
from config.config import cfg as config
from flask_httpauth import HTTPBasicAuth
from flask import request, Response
from common import authorization as au
from service import utils_serv as utl
from flask import Blueprint
from mdata import metadata as md
import json

app_view = Blueprint('app_view', __name__)

logger = config.logger
auth = HTTPBasicAuth()
domain_root = '/md'
GLOBAL_VIEW_ID = "$_VIEW_ID"


# 验证token
@auth.verify_password
def verify_password(username, password):
    bool = au.verify_password(username, password)
    if bool:
        utl.get_login_user_privilege()
    return bool


@app_view.route(domain_root + '/app_profile', methods=['GET'])
@auth.login_required
def env_profile():
    return config.ENV


# 实体元数据对象清单查询,入参：{}
@app_view.route(domain_root + '/services/queryViewList', methods=['POST', 'GET'])
@auth.login_required
def query_view_list():
    data = None
    re = None
    try:
        data = utl.request_parse(request)
        md_entity_id = None
        md_entity_code = "data_views"
        user = utl.get_login_user()
        tenant_id = user.get("tenant_id")
        if md_entity_id is None and md_entity_code is not None:
            (res, msg) = utl.getEntityIDByCode(tenant_id, [md_entity_code], data)
            if (res is not None and len(res) > 0):
                md_entity_id = res[0].get("md_entity_id")
                public_flag = res[0].get("public_flag")
        if md_entity_id is None:
            msg = "queryViewList ,md_entity_code not exists,please checked."
            re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                       message=msg)
            return Response(json.dumps(re), mimetype='application/json')

        re = utl.sql_execute_method(tenant_id, md_entity_id, utl.SERVICE_METHOD_GET, "findEntity", data_list=None,
                                    where_list=None, parent_entity_id=None)
        logger.info('queryViewList, Params:{},result:{}'.format(data, re))
        return Response(json.dumps(re), mimetype='application/json')
    except Exception as ex:
        msg = "queryViewList error.input:{},message:{}".format(data, ex)
        logger.error(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
        # raise ex
    finally:
        pass

# 视图查询
@app_view.route(domain_root + '/services/queryView', methods=['POST', 'GET'])
@auth.login_required
def query_view():
    re = None
    data = None
    try:
        data = utl.request_parse(request)
        view_id = data.get(GLOBAL_VIEW_ID)
        page_size = data.get('page_size')
        current_page = data.get('current_page')
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
        user = utl.get_login_user()
        tenant_id = user.get("tenant_id")
        re = utl.sql_execute_method(tenant_id, view_id, utl.SERVICE_METHOD_VIEW, "queryView", data_list=None,
                                    where_list=[data])

        logger.info('view result:{}'.format(re))
        return Response(json.dumps(re), mimetype='application/json')
    except Exception as ex:
        msg = "query View error.input:{},message:{}".format(data, ex)
        logger.error(msg)
        re = md.exec_output_status(type=utl.SERVICE_METHOD_GET, status=md.DB_EXEC_STATUS_FAIL, rows=0, data=None,
                                   message=msg)
        return Response(json.dumps(re), mimetype='application/json')
        # raise ex
    finally:
        pass
