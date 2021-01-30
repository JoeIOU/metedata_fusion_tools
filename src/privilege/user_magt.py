# ####user_magt.py
# 用户管理和维护
from db.db_conn import db_connection_metedata as db_md
from config.config import cfg as config

logger = config.logger


# 用户ID+租户
def get_user_tenant(user_id):
    if user_id is None:
        logger.warning("get_user_tenant,[user_id] should not not be None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select user_id,tenant_id,account_number,user_name from users where active_flag='Y' and user_id=%s"
    cursor.execute(sql, args=(user_id,))
    result = cursor.fetchall()
    logger.info("current user:{}".format(result))
    user = None
    if result is not None and len(result) > 0:
        user = result[0]
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return user


# 用户查询信息
def get_user(user_account):
    if user_account is None:
        logger.warning("get_user,user_account is None")
        return None
    conn = db_md()
    cursor = conn.cursor()
    sql = "select user_id,tenant_id,account_number,user_name from users where active_flag='Y' and account_number=%s"
    cursor.execute(sql, args=(user_account,))
    result = cursor.fetchone()
    logger.info("get current user:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result
