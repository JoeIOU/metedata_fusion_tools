# neo4j_conn.py
# 图数据库连接池
from py2neo import Graph
from config.config import cfg as config

graph = None
graph1 = None


def get_graph():
    url1 = config.LOGIN_NEO4J['url']
    name = config.LOGIN_NEO4J['user']
    pwd = config.LOGIN_NEO4J['password']
    # grph = Graph(uri="http://localhost:7474/db/data", auth=("neo4j", "123456"))
    grph = Graph(uri=url1, auth=(name, pwd))
    return grph


def get_graph1():
    url1 = config.LOGIN_NEO4J1['url']
    name = config.LOGIN_NEO4J1['user']
    pwd = config.LOGIN_NEO4J1['password']
    # grph1 = Graph(uri="http://localhost:7475/db/data", auth=("neo4j", "123456"))
    grph1 = Graph(uri=url1, auth=(name, pwd))
    return grph1


def neo4j_graph(option=1):
    global graph
    global graph1
    if option == 1:
        if graph is None:
            graph = get_graph()
        return graph
    else:
        if graph1 is None:
            graph1 = get_graph1()
        return graph1
