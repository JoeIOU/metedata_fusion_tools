# neo4j_conn.py
# 图数据库连接池
from py2neo import Graph
from config.config import cfg as config

graph = None


def get_graph():
    url1 = config.LOGIN_NEO4J['url']
    name = config.LOGIN_NEO4J['user']
    pwd = config.LOGIN_NEO4J['password']
    # graph = Graph(uri="http://localhost:7474/db/data", auth=("neo4j", "123456"))
    graph = Graph(uri=url1, auth=(name, pwd))
    return graph


def neo4j_graph():
    global graph
    if graph is None:
        graph = get_graph()
    return graph
