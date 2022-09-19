#####neo4j_service.py
from json import dumps
from flask import Response, request
from db.neo4j_conn import neo4j_graph as graph
from config.config import cfg as config
from service import utils_serv as utl
from flask_httpauth import HTTPBasicAuth
from common import authorization as au
from httpserver import httpserver

logger = config.logger
app = httpserver.getApp()
auth = HTTPBasicAuth()

domain_root = '/md/graph'


# 验证token
@auth.verify_password
def verify_password(username, password):
    bool = au.verify_password(username, password)
    # if bool:
    #     utl.get_login_user_privilege()
    return bool


def serialize_model(model):
    release = model['entity_id']
    s_ver = ""
    if release is not None:
        s_ver = str(release)
    return {
        'entity_id': model['entity_id'],
        'entity_code': model['entity_code'],
        'title': model['name'],
        'entity_name': model['entity_name'],
        'entity_desc': model['entity_desc'],
        'schema': model['schema']
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
        'name': cast[0],
        'label': cast[1],
        'relation_id': cast[2],
        'relation_type': cast[3],
        'relation_desc': cast[4],
        'from_entity_name': cast[5],
        'from_fields_name': cast[6],
        'to_entity_name': cast[7],
        'to_fields_name': cast[8]
    }


@app.route(domain_root + "/graph/<title>/<flag>")
@auth.login_required
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


@app.route(domain_root + "/search")
@auth.login_required
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        user = utl.get_login_user()
        tenant_id = user.get("tenant_id")
        # user_id = user.get("user_id")
        q_str = "(?i).*" + q + ".*"
        cql = "MATCH (m) WHERE (m.name =~ '{}' or m.entity_code=~ '{}')and((m.public_flag is null and m.tenant_id is null) or m.public_flag='Y' or  m.tenant_id={}) RETURN m".format(
            q_str, q_str, tenant_id)
        results = graph().run(cql)

        return Response(dumps([serialize_model(record['m']) for record in results]),
                        mimetype="application/json")


@app.route(domain_root + "/search_shortest_path")
@auth.login_required
def search_shortest_path():
    try:
        q = request.args["q"]
        to = request.args["to"]
        flag = request.args["flag"]
        sfrom = ""
        sto = ""
        # flag==0,则是all，==1则是Child子类关系查询，==2其他则是父类Parent关系查询
        if flag is not None and flag == "1":
            sfrom = ""
            sto = ">"
        elif flag is not None and flag == "2":
            sfrom = "<"
            sto = ""
    except KeyError:
        return []
    else:
        cql = "MATCH (p1 {name:'%s'}),(p2{name:'%s'}),p=shortestpath((p1)%s-[r*..10]-%s(p2))RETURN r,p" % (
            q, to, sfrom, sto)
        result = graph().run(cql)
        nodes, relationships = relationship_mapping1(result)
        data = combine_data(nodes, relationships)
        logger.info("search_shortest_path,graph data:{}".format(data))
        return Response(dumps(data), mimetype="application/json")


def query_graph_rel(medel_name, sfrom, sto):
    if sfrom is None:
        sfrom = ""
    if sto is None:
        sto = ""
    cql = "MATCH p=(n{name:'%s'})%s-[r]-%s(m) RETURN r,p LIMIT 100" % (medel_name, sfrom, sto)
    result = graph().run(cql)
    return relationship_mapping1(result)


# def relationship_mapping(path):
#     if path is None:
#         return None, None
#     nodes = []
#     relationships = []
#     id_list = []
#     user = utl.get_login_user()
#     tenant_id = user.get("tenant_id")
#     # user_id = user.get("user_id")
#     not_privilege_list = []
#     if path is not None:
#         for res in path:
#             for paths in res:
#                 logger.info("path:{}".format(paths))
#                 for node in paths.nodes:
#                     # 权限判断
#                     bool = have_entity_privilege(tenant_id, node)
#                     if (not bool):
#                         not_privilege_list.append(node.get('entity_id'))
#                         continue
#                     d_start, is_exist = node2dict(node, id_list)
#                     if not is_exist and d_start is not None:
#                         nodes.append(d_start)
#                 relationship_list = paths.relationships
#                 for relationship in relationship_list:
#                     from_enty_id = relationship['from_entity_id']
#                     to_enty_id = relationship['to_entity_id']
#                     is_true = False
#                     for no_priv_entity_id in not_privilege_list:
#                         if (from_enty_id == no_priv_entity_id or to_enty_id == no_priv_entity_id):
#                             is_true = True
#                             break
#                     if is_true:
#                         continue
#                     d_rel = relationship2dict(relationship)
#                     if d_rel is not None:
#                         relationships.append(d_rel)
#         logger.info("relation_info:{},{}".format(nodes, relationships))
#     return nodes, relationships


def relationship_mapping1(path):
    if path is None:
        return None, None
    nodes = []
    relationships = []
    id_list = []
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    # user_id = user.get("user_id")
    not_privilege_list = []
    if path is not None:
        # for res in path:
        if path is not None:
            for paths in path:
                logger.info("path:{}".format(paths))
                if paths['p'] is not None:
                    for node in paths['p'].nodes:
                        # 权限判断
                        bool = have_entity_privilege(tenant_id, node)
                        if (not bool):
                            not_privilege_list.append(node.get('entity_id'))
                            continue
                        d_start, is_exist = node2dict(node, id_list)
                        if not is_exist and d_start is not None:
                            nodes.append(d_start)
                if paths['r'] is not None:
                    relat = paths['r']
                    rel1 = []
                    if isinstance(relat, dict):
                        ls = []
                        ls.append(relat)
                        rel1 = ls
                    elif isinstance(relat, list):
                        rel1 = relat
                    if rel1 is not None:
                        for relationship in rel1:
                            from_enty_id = relationship['from_entity_id']
                            to_enty_id = relationship['to_entity_id']
                            is_true = False
                            for no_priv_entity_id in not_privilege_list:
                                if (from_enty_id == no_priv_entity_id or to_enty_id == no_priv_entity_id):
                                    is_true = True
                                    break
                            if is_true:
                                continue
                            d_rel = relationship2dict(relationship)
                            if d_rel is not None:
                                relationships.append(d_rel)
        logger.info("relation_info:{},{}".format(nodes, relationships))
    return nodes, relationships


def have_entity_privilege(tenant_id, node):
    have_bool = False
    ten_id = node.get('tenant_id')
    flag = node.get('public_flag')
    if (ten_id is None and flag is None):
        have_bool = True
    elif (ten_id == tenant_id or flag == 'Y'):
        have_bool = True
    return have_bool


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
    # d["title"] = label
    d["properties"] = properties
    if id_list.count(id) <= 0:
        id_list.append(id)
        is_exists = False
    return d, is_exists


def gen_new_id(old_id, name):
    id = ""
    if id is not None:
        id = str(old_id)
    if id is not None and len(id) > 2:
        id = id[len(id) - 2:]
    s = name
    id = s + "(*" + id + ")"
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
    cql = "MATCH (m {name:'%s'}) OPTIONAL MATCH (m)%s-[r]-%s(n) RETURN m.name as name,m.entity_id as entity_id,m.entity_code as title,m.tenant_id as tenant_id,m.public_flag as public_flag," \
          "COLLECT([r.name, r.label,r.relation_id,r.relation_type,r.relation_desc,r.from_entity_id,r.from_entity_name,r.from_fields_name,r.to_entity_id,r.to_entity_name,r.to_fields_name]) AS cast LIMIT 100" % (
              title, sfrom, sto)
    result = graph().run(cql)
    user = utl.get_login_user()
    tenant_id = user.get("tenant_id")
    re_list = []
    for item in result:
        dict1 = {}
        dict1["title"] = item.get('title')
        dict1["name"] = item.get('name')
        # ten_id=item.get('tenant_id')
        # public_flag=item.get("public_flag")
        bool = have_entity_privilege(tenant_id, item)
        if (not bool):
            continue
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


@app.route(domain_root + "/relation/<title>/<flag>")
@auth.login_required
def get_relation(title, flag):
    dict1 = query_relation(title, flag)
    return Response(dumps(dict1), mimetype="application/json")


if __name__ == '__main__':
    app.run(port=8080, host="localhost", threaded=True)  # 8080
