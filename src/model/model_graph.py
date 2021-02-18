# model_graph.py
# ==元数据关系转换成Neo4j图数据库关系
from py2neo import Node, Relationship, NodeMatcher, Subgraph
from db.neo4j_conn import neo4j_graph as graph
from config.config import cfg as config

DATA_ENTITY = "ENTITY"
logger = config.logger
graph = graph()


def create_object(graph, label, name, **kwargs):
    a = Node(label, name=name, **kwargs)
    graph.create(a)


# 创建图数据库实体对象
def create_object_from_metadata(entity_list):
    if entity_list is None:
        return None
    cql_create_node_template = "CREATE ({name}:{labels}:%s {fields})" % (DATA_ENTITY)
    kv_template = "{key}:{value}"
    nm = None
    for item in entity_list:
        name = item.get("name")
        labels = item.get("label")
        fileds_str = None
        for key in item.keys():
            value = item[key]
            if not (isinstance(value, int) or isinstance(value, float)):
                value = "'{}'".format(value)
            if fileds_str is None:
                fileds_str = kv_template.format(key=key, value=value)
            else:
                fileds_str += "," + kv_template.format(key=key, value=value)
        fileds_str = "{" + fileds_str + "}"
        cql = cql_create_node_template.format(name=name, labels=labels, fields=fileds_str)

        nm = graph.run(cql)
    if nm is None:
        logger.warning("create_object_from_metadata,create node failed:{}".format(entity_list))
    else:
        logger.info("create_object_from_metadata,create node success:{}".format(entity_list))
    return entity_list


# 创建图数据库实体对象关系
def create_object_rel_from_metadata(entity_rel_list):
    if entity_rel_list is None or len(entity_rel_list) <= 0:
        return None
    ii = 0
    ls_obj = []
    nm = NodeMatcher(graph)
    for item in entity_rel_list:
        rel_type = item.get("label")
        rel_flag = item.get("name")
        rel_id = item.get("relation_id")
        rel_desc = item.get("relation_desc")
        rel_type = item.get("relation_type")
        frm_md_entity_id = item.get("from_entity_id")
        frm_md_entity_name = item.get("from_entity_name")
        frm_md_entity_code = item.get("from_entity_code")
        frm_md_fields_id = item.get("from_fields_id")
        frm_md_fields_name = item.get("from_fields_name")
        to_md_entity_id = item.get("to_entity_id")
        to_md_entity_name = item.get("to_entity_name")
        to_md_entity_code = item.get("to_entity_code")
        to_md_fields_id = item.get("to_fields_id")
        to_md_fields_name = item.get("to_fields_name")
        rel_type_new = "{}({})".format(rel_type, to_md_fields_name)
        item["relation_type"] = rel_type_new
        item["label"] = rel_type_new

        node1 = nm.match(frm_md_entity_code, name=frm_md_entity_code).first()
        node2 = nm.match(to_md_entity_code, name=to_md_entity_code).first()
        if node1 is None or node2 is None:
            continue
        properties = item
        node1_vs_node2 = Relationship(node1, rel_type_new, node2, **properties)
        ls_obj.append(node1_vs_node2)
        ii += 1
        if ii >= 100:
            A = Subgraph(relationships=ls_obj)
            graph.create(A)
            ls_obj = []
            ii = 0
    if len(ls_obj) > 0:
        A = Subgraph(relationships=ls_obj)
        graph.create(A)
    if nm is None:
        logger.warning("create_object_rel_from_metadata,create node failed:{}".format(entity_rel_list))
    else:
        logger.info("create_object_rel_from_metadata,create node success:{}".format(entity_rel_list))
    return entity_rel_list


def create_unique_index(label, field):
    # cql="CREATE CONSTRAINT ON (cc:User) ASSERT cc.name IS UNIQUE"
    cql = "CREATE CONSTRAINT ON (cc:{}) ASSERT cc.{} IS UNIQUE".format(label, field)
    nm = graph.run(cql)
    return nm.data()


def query_node(graph, label):
    cql = "MATCH (d:{}) return d".format(label)
    nm = graph.run(cql)
    data = nm.data()
    logger.info("query_node,result:{}".format(data))
    return data


def create_relation(graph):
    nm = NodeMatcher(graph)
    user = nm.match("User", name="user").first()
    role = nm.match("Role", name="role").first()
    group = nm.match("Group", name="group").first()
    tenant = nm.match("Tenant", name="tenant").first()

    r1 = Relationship(user, 'OWN', role)
    r2 = Relationship(user, 'belongTo', group)
    r1 = Relationship(group, 'belongTo', tenant)
    r2 = Relationship(user, 'belongTo', tenant)
    r3 = Relationship(role, 'belongTo', tenant)
    rr = r1 | r2 | r3
    graph.create(rr)

    
# 查询2个节点间的关系（10层内关系）
def query_relation_between_entity(graph, node_label1, node_label2):
    if graph is None or node_label1 is None or node_label2 is None:
        return None
    cql = "match data=(na:{})-[*1..10]-(nb:{}) return data".format(node_label1, node_label2)
    nm = graph.run(cql)
    data = nm.data()
    logger.info("query_relation_between_entity,result:{}".format(data))
    return data


# 查询某个节点间的关系（1层内关系）
def query_relation_by_node_label(graph, node_label):
    if graph is None or node_label is None:
        return None
    cql = "match data=(m:{})-[*1]-(n) return data".format(node_label)
    nm = graph.run(cql)
    data = nm.data()
    logger.info("query_relation_by_node_label,result:{}".format(data))
    return data


# 3个字母以上名称模糊查询所有节点
def query_all_node_by_name(graph, node_name):
    if graph is None or node_name is None or len(node_name) < 3:
        return None
    cql = "match (n) where n.name =~'(?i).*{}.*' return n".format(node_name)
    nm = graph.run(cql)
    data = nm.data()
    logger.info("query_all_node_by_name,result:{}".format(data))
    return data

if __name__ == "__main__":
    # create_object(graph)
    entity_list = []
    obj = {"name": "Mark1", "label": "Person", "Age": 20}
    entity_list.append(obj)
    # re = create_object_from_metadata(graph, entity_list)

    # re = create_object(graph, label="ABC", name="test", age=120,gendar="M")
    
    # data = query_relation_between_entity(graph, "SALE_CONTRACT_T", "SALE_CFG_BOQ_T")
    # logger.info("query_relation_between_entity,result:{}".format(data))

    data = query_all_node_by_name(graph, "cfg")
    # logger.info("query_all_node_like_label,result:{}".format(data))
    pass
