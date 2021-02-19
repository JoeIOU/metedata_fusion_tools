#####neo4j_service.py
from json import dumps
from flask import Flask, Response, request
from db.neo4j_conn import neo4j_graph as graph
from config.config import cfg as config

# from httpserver import httpserver

logger = config.logger
graph = graph()
app = Flask(__name__, static_url_path='/static/')
# app.static_url_path='/static/'
# app = httpserver.getApp()

# domain_root = '/md'

DATA_ENTITY = "ENTITY"


@app.route("/")
def get_index():
    return app.send_static_file('index.html')


def serialize_model(model):
    release = model['entity_id']
    s_ver = ""
    if release is not None:
        s_ver = str(release)
    return {
        'id': model['id'],
        'title': model['entity_code'],
        'name': model['name'],
        'released': s_ver
    }


def serialize_model_path(model):
    release = model['entity_id']
    s_ver = ""
    if release is not None:
        s_ver = str(release)
    return {
        'id': model['id'],
        'title': model['entity_code'],
        'name': model['name'],
        'released': s_ver
    }


def serialize_cast(cast):
    return {
        'REL_TABLE': cast[0],
        'REL_TYPE': cast[1],
        'REL_PK': cast[2],
        'REL_FK': cast[3]
    }


@app.route("/graph/<title>/<flag>")
def get_graph(title, flag):
    if title is None or title == '':
        return None
    result = query_relation_graph(title, flag)
    return Response(dumps(result), mimetype="application/json")


def query_relation_graph(title, flag):
    sfrom = ""
    sto = ""
    # flag==0,则是all，==1则是Child子类关系查询，==2其他则是父类Parent关系查询
    if flag is not None and flag == "1":
        sfrom = ""
        sto = ">"
    elif flag is not None and flag == "2":
        sfrom = "<"
        sto = ""
    nodes, relationships = query_graph_rel(title, sfrom, sto)
    data = combine_data(nodes, relationships)
    logger.info("graph data:{}".format(data))
    return data


@app.route("/search")
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        q_str = "(?i).*" + q + ".*"
        cql = "MATCH (m:ENTITY) WHERE m.name =~ '{}' or m.entity_code=~ '{}' RETURN m".format(q_str, q_str)
        results = graph.run(cql)

        return Response(dumps([serialize_model(record['m']) for record in results]),
                        mimetype="application/json")


@app.route("/search_shortest_path")
def search_shortest_path():
    try:
        q = request.args["q"]
        to = request.args["to"]
    except KeyError:
        return []
    else:
        cql = "MATCH (p1:ENTITY {label:'%s'}),(p2:ENTITY{label:'%s'}),p=shortestpath((p1)-[*..10]-(p2))RETURN p" % (
            q, to)
        result = graph.run(cql)
        nodes, relationships = relationship_mapping(result)
        data = combine_data(nodes, relationships)
        logger.info("search_shortest_path,graph data:{}".format(data))
        return Response(dumps(data), mimetype="application/json")


def query_graph_rel(medel_name, sfrom, sto):
    if sfrom is None:
        sfrom = ""
    if sto is None:
        sto = ""
    cql = "MATCH p=(n:ENTITY{name:'%s'})%s-[r]-%s(m) RETURN p LIMIT 100" % (medel_name, sfrom, sto)
    result = graph.run(cql)
    return relationship_mapping(result)


def relationship_mapping(path):
    if path is None:
        return None, None
    nodes = []
    relationships = []
    id_list = []
    if path is not None:
        for res in path:
            for paths in res:
                logger.info(paths)
                for node in paths.nodes:
                    d_start, is_exist = node2dict(node, id_list)
                    if not is_exist and d_start is not None:
                        nodes.append(d_start)
                relationship_list = paths.relationships
                for relationship in relationship_list:
                    d_rel = relationship2dict(relationship)
                    if d_rel is not None:
                        relationships.append(d_rel)
        logger.info("relation_info:{},{}".format(nodes, relationships))
    return nodes, relationships


def combine_data(nodes, relationships):
    d_total = {}
    graph_dict = {}
    graph_dict["nodes"] = nodes
    graph_dict["relationships"] = relationships
    dict1 = {}
    dict1["graph"] = graph_dict
    columns = ["Model", "Entity"]
    result_dict = {}
    result_dict["columns"] = columns
    result_dict["data"] = [dict1]
    # result_dict[""]=
    d_total["results"] = [result_dict]
    d_total["errors"] = []
    return d_total


def node2dict(node, id_list):
    d = {}
    if id_list is None:
        id_list = []
    id = "0"
    label = []
    is_exists = True
    properties = {}
    for (ID, field) in enumerate(node):
        if field is not None and field == "label":
            label.append(node[field])
        if field is not None and field == "entity_id":
            properties["_id"] = str(node[field])
            oid = node[field]
            s = node["entity_name"]
            id = gen_new_id(oid, s)
        if field is not None and (field == "entity_id" or field == "entity_code" or field == "entity_name"):
            continue
        properties[field] = str(node[field])
    d["id"] = id
    d["labels"] = label
    d["title"] = label
    d["properties"] = properties
    if id_list.count(id) <= 0:
        id_list.append(id)
        is_exists = False
    return d, is_exists


def gen_new_id(old_id, name):
    id = ""
    if id is not None:
        id = str(old_id)
    if id is not None and len(id) > 3:
        id = id[len(id) - 3:]
    s = name
    id = s + "(" + id + ")"
    return id


def relationship2dict(relationship):
    d = {}
    id = 0
    type, from_id, to_id = None, None, None
    properties = {}
    for (ID, field) in enumerate(relationship):
        if field is not None and field == "relation_type":
            type = relationship[field]
        if field is not None and field == "from_entity_id":
            oid = str(relationship[field])
            s = relationship["from_entity_name"]
            from_id = gen_new_id(oid, s)
        if field is not None and field == "to_entity_id":
            oid = str(relationship[field])
            s = relationship["to_entity_name"]
            to_id = gen_new_id(oid, s)
        if field is not None and field == "relation_id":
            id = str(relationship[field])
        if field is not None and (field == "id" or field == "name" or field == "label" or
                                  field == "relation_id" or field == "relation_type" or field == "relation_desc"
                                  or field == "from_entity_id" or field == "from_entity_code" or field == "from_fields_id"
                                  or field == "to_entity_id" or field == "to_entity_code" or field == "to_fields_id"):
            continue
        properties[field] = str(relationship[field])
    d["id"] = id
    d["type"] = type
    d["startNode"] = from_id
    d["endNode"] = to_id
    d["properties"] = properties
    return d


def query_relation(title, flag):
    sfrom = ""
    sto = ""
    # flag==0,则是all，==1则是Child子类关系查询，==2其他则是父类Parent关系查询
    if flag is not None and flag == "1":
        sfrom = ""
        sto = ">"
    elif flag is not None and flag == "2":
        sfrom = "<"
        sto = ""
    cql = "MATCH (m:ENTITY {entity_code:'%s'}) OPTIONAL MATCH (m)%s-[r]-%s(n:ENTITY) RETURN m.name as name,m.entity_code as title," \
          "COLLECT([n.name, r.label,r.from_fields_name,r.to_fields_name]) AS cast LIMIT 100" % (title, sfrom, sto)
    result = graph.run(cql)
    re_list = []
    for item in result:
        dict1 = {}
        dict1["title"] = item.get('title')
        dict1["name"] = item.get('name')
        cast = item.get('cast')
        if cast is not None:
            li_cast = []
            for member in cast:
                li_cast.append(serialize_cast(member))
            dict1["cast"] = li_cast
        re_list.append(dict1)
    if re_list is not None and len(re_list) > 0:
        dict2 = re_list[0]
    else:
        dict2 = None
    return dict2


@app.route("/relation/<title>/<flag>")
def get_relation(title, flag):
    dict1 = query_relation(title, flag)
    return Response(dumps(dict1), mimetype="application/json")


if __name__ == '__main__':
    # httpserver.startWebServer()
    app.run(port=8080)
