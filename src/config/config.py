# ######config.py
# -*- coding:utf-8 -*-
import os, sys, logging

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

from common import logger
from easydict import EasyDict as edict

__C = edict()
cfg = __C

# 环境
__C.ENV = "dev"
# __C.ENV = "sit"
# __C.ENV = "uat"
# __C.ENV = "pro"

# md URL
__C.__MD_URL = {"dev": "http://localhost:8080/isales/knowme",
                "sit": "http://isales-alpha.huawei.com/isales/knowme",
                "uat": "http://isales-beta.huawei.com/isales/knowme",
                "pro": "http://isales.huawei.com/isales/knowme"}

# 日志级别
# __C.LOG_LEVEL = logging.DEBUG
__C.LOG_LEVEL = logging.INFO
# __C.LOG_LEVEL = logging.NOTICE
# __C.LOG_LEVEL = logging.WARNING
# __C.LOG_LEVEL = logging.ERROR
# __C.LOG_LEVEL = logging.CRITICAL
# __C.LOG_LEVEL = logging.ALERT
# __C.LOG_LEVEL = logging.EMERGENCY

# 日志格式
__C.LOG_FORMAT = "%(asctime)s - [%(levelname)s] %(message)s"
__C.LOG_FORMAT_ERROR = "%(asctime)s - [%(levelname)s] %(filename)s[:%(lineno)d] - %(message)s"

# 日期格式
__C.DATE_FORMAT = "%Y-%m-%d"
__C.TIME_FORMAT = "%H:%M:%S"
__C.DATE_TIME_FORMAT = __C.DATE_FORMAT + " " + __C.TIME_FORMAT

# 日志文件
__C.LOG_PATH = "/log/"
if not os.path.exists(__C.LOG_PATH):
    os.makedirs(__C.LOG_PATH)

# 日志设置
__C.logger = logger.init(__C.LOG_FORMAT, __C.LOG_FORMAT_ERROR, __C.LOG_LEVEL, __C.LOG_PATH, __C.ENV,
                         __C.DATE_TIME_FORMAT)
log = __C.logger
log.info("Active profile is %s", __C.ENV)

# 默认Login登录设置
__C.__LOGIN = {"dev": {"url": "https://login-b.dm.com/login/login.do", "user": "test1",
                       "password": ""},
               "sit": {"url": "https://login-b.dm.com/login/login.do", "user": "test1",
                       "password": ""},
               "uat": {"url": "https://login-b.dm.com/login/login.do", "user": "test1",
                       "password": ""},
               "pro": {"url": "https://login.dm.com/login/login.do", "user": "user1",
                       "password": ""}}

# 默认Noe4j Login登录设置
__C.__LOGIN_NEO4J = {"dev": {"url": "http://localhost:7474/db/data", "user": "neo4j",
                             "password": "123456"},
                     "sit": {"url": "http://localhost:7474/db/data", "user": "neo4j",
                             "password": "123456"},
                     "uat": {"url": "http://localhost:7474/db/data", "user": "neo4j",
                             "password": ""},
                     "pro": {"url": "http://localhost:7474/db/data", "user": "neo4j",
                             "password": ""}}

# APP ID和Token配置
__C.__AP_ID = {"dev": "ap_00000123", "pro": "ap_00000123"}
# 数据库配置
__C.__DB_CONFIG = {"dev": {
    'host': 'localhost',
    'user': 'root',
    'password': "123456",
    'port': 3306,
    'database': 'test',
    'charset': 'utf8',
    'pool': "mypool",
    'pool_size': 30
},
    "pro": {
        'host': '10.65.31.250',
        'user': 'mobile2',
        'password': 'Pr0d1234',
        'port': 3306,
        'database': 'mobile_pro',
        'charset': 'utf8',
        'pool': "mypool",
        'pool_size': 30
    }
}


def getEnv():
    return __C.ENV


# 初始化环境变量
def dict_inv_set(inv):
    __C.ENV = inv
    # 参数初始化
    # __C.AP_ID = __C.__AP_ID["pro" if __C.ENV == "pro" else "dev"]
    # __C.DB_CONFIG = __C.__DB_CONFIG[__C.ENV]

    # 默认登录信息
    # __C.LOGIN = __C.__LOGIN["pro" if __C.ENV == "pro" else "dev"]
    # __C.SOA_URL = __C.__SOA_URL["pro" if __C.ENV == "pro" else "dev"]

    __C.LOGIN_NEO4J = __C.__LOGIN_NEO4J[getEnv()]


dict_inv_set(__C.ENV)
