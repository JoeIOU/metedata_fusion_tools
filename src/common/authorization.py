# ####authorization.py
from flask import Flask, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import TimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_cors import CORS
import re
from config.config import cfg as config
from privilege import user_mngt as ur
from common import cache
import datetime

logger = config.logger

# 密钥，可随意修改
SECRET_KEY = 'J@#oabcdefghijklmm@#H33@kwl!@jK%22W#Etty%@'

app = Flask(__name__)
CORS(app, supports_credentials=True)
auth = HTTPBasicAuth()


# 生成token, 有效时间为600min
def generate_auth_token(user_id, expiration=36000):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    utc = datetime.datetime.utcnow()
    timestamp = utc.timestamp()
    utc_msecond = int(round(timestamp * 1000))
    expire_time = utc_msecond + (expiration * 1000)
    re = {'user_id': user_id}
    logger.info('token:{}'.format(re))
    return (s.dumps(re), expire_time)


# 解析token
def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    # token正确
    try:
        data = s.loads(token)
        return data
    # token过期
    except SignatureExpired:
        return None
    # token错误
    except BadSignature:
        return None


def login_verify(user_account, password):
    if user_account is None or password is None:
        return None
    login_flag = False
    # -------------
    # verify code...
    # --------------

    # if login_flag:
    res = None
    if True:
        res = ur.get_user(user_account)
        logger.info("login success,user info:{}".format(res))
    return res


# 验证token
@auth.verify_password
def verify_password(username, password, force=False):
    # 先验证token
    user_id = re.sub(r'^"|"$', '', username)
    user = None
    token = None
    if not force:
        token = verify_auth_token(user_id)
        if token is not None:
            user_id = token.get('user_id')
    # 如果token不存在，验证用户id与密码是否匹配
    if not token:
        user = login_verify(user_id, password)
        # 如果用户id与密码对应不上，返回False
        if not user:
            logger.warning("the user[{}] login failed,the user account or password is wrong.".format(user_id))
            return False
        g.user = user
        cache.push(user_id, user)
    else:
        if cache.get(user_id) is None:
            new_user = ur.get_user(user_id)
            cache.push(user_id, new_user)
    if user_id is None:
        logger.warning("the user[{}] login failed,the user account or password is wrong.".format(username))
        return False
    g.user_id = user_id
    return True


if __name__ == '__main__':
    # logger.info("tokenDecode:{}".format('s'))
    generate_auth_token('test1', 36000)
