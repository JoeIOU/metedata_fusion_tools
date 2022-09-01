# ####authorization.py
from flask import Flask, g
from flask_httpauth import HTTPBasicAuth
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import TimedSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired
from flask_cors import CORS
import re
from config.config import cfg as config
from privilege import user_mngt as ur
from common import cache
import datetime
import time
import base64
import hmac

logger = config.logger

# 密钥，可随意修改
SECRET_KEY = 'J@#oabcdefghijklmm@#H33@kwl!@jK%22W#Etty%@'

app = Flask(__name__)
CORS(app, supports_credentials=True)
auth = HTTPBasicAuth()


# 生成token, 有效时间为600min
# def generate_auth_token(user_id, expiration=36000):
#     s = Serializer(SECRET_KEY, expires_in=expiration)
#     utc = datetime.datetime.utcnow()
#     timestamp = utc.timestamp()
#     utc_msecond = int(round(timestamp * 1000))
#     expire_time = utc_msecond + (expiration * 1000)
#     re = {'user_id': user_id}
#     logger.info('token:{}'.format(re))
#     return (s.dumps(re), expire_time)


def generate_auth_token(key, expire=3600):
    r'''
    @Args:
     key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
     expire: int(最大有效时间，单位为s)
    @Return:
     state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return (b64_token.decode("utf-8"), expire)


# 解析token
# def verify_auth_token(token):
#     s = Serializer(SECRET_KEY)
#     # token正确
#     try:
#         data = s.loads(token)
#         return data
#     # token过期
#     except SignatureExpired:
#         return None
#     # token错误
#     except BadSignature:
#         return None

def verify_auth_token(token):
    r'''
    @Args:
     key: str
     token: str
    @Returns:
     boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return None
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return None
    known_sha1_tsstr = token_list[1]
    # sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    # calc_sha1_tsstr = sha1.hexdigest()
    # if calc_sha1_tsstr != known_sha1_tsstr:
    # token certification failed
    #  return False
    # token certification success
    return known_sha1_tsstr


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
    (s, ex) = generate_auth_token('test1', 36000)
    logger.info("token:{}".format(s))
    ss = verify_auth_token(s)
    logger.info("tokenDecode:{}".format(ss))
