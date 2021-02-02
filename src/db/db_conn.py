# db_conn.py
from dbutils.pooled_db import PooledDB
import pymysql
import cx_Oracle as oracle
# import psycopg2 as pg

# 元数据mysql连接池
POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=50,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=50,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='test',
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8'
)
# mySQL业务数据连接池
POOL1 = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=50,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=50,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='test',
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8'
)
# oracle业务数据连接池
POOL_ORA = PooledDB(
    creator=oracle,  # 使用链接数据库的模块
    maxconnections=5,  # 连接池允许的最大连接数，0和None表示没有限制
    mincached=2,  # 初始化时，连接池至少创建的空闲的连接，0表示不创建
    maxcached=3,  # 连接池空闲的最多连接数，0和None表示没有限制
    maxshared=0,
    # 连接池中最多共享的连接数量，0和None表示全部共享，ps:其实并没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
    blocking=True,  # 链接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，False表示不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表
    ping=0,  # ping Mysql 服务端，检查服务是否可用
    user='salequery',
    password='Pr0d1234',
    dsn='(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=kwetsp47172-cls)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=SALEBETA.huawei.com)))',
    encoding='utf-8'
)

# PG连接池
POOL_PG = PooledDB(
    creator=pg,  # 使用连接数据库的模块 psycopg2
    maxconnections=6,  # 连接池允许的最大连接数，0 和 None 表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0 表示不创建
    maxcached=4,  # 链接池中最多闲置的链接，0 和 None 不限制
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None 表示无限制
    setsession=[],  # 开始会话前执行的命令列表
    host='127.0.0.1',
    port='5432',
    user='postgres',
    password='123456',
    database='test')


# 元数据连接池
def db_connection_metedata():
    conn = POOL.connection()
    return conn


# mySQL业务数据连接池
def db_connection_data():
    conn = POOL1.connection()
    return conn


# Oracle业务数据连接池
def db_connection_oracle():
    # user = "salequery"
    # pwd = "Pr0d1234"
    # dns = "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=kwetsp47172-cls)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=SALEBETA.huawei.com)))"
    # conn = oracle.connect(user, pwd, dns)
    # 获取数据库连接的方式
    conn = POOL_ORA.connection()
    return conn


# PG业务数据连接池
def db_connection_pg():
    # 获取数据库连接的方式
    conn = POOL_PG.connection()
    return conn


if __name__ == '__main__':
    print()
