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
