# #view_service.py
from config.config import cfg as config
from flask_httpauth import HTTPBasicAuth
from common import authorization as au
from service import utils_serv as utl
from flask import Blueprint

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
