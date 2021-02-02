# neo4j_conn.py
# 图数据库连接池
from py2neo import Graph

graph = None

def get_graph():
    graph = Graph(uri="http://localhost:7474/db/data", username="neo4j", password="123456")
    return graph

def neo4j_graph():
    global graph
    if graph is None:
        graph = get_graph()
    return graph
