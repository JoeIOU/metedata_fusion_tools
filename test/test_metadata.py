# ######test_metadata.py
from mdata import metadata_initialize as mdi, metadata as md
from data import data_view as dv
from config.config import cfg as config
from privilege import user_mngt as ur
from model import erwin_model_graph as emg

logger = config.logger

import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


def test_md():
    user = ur.get_user_tenant(1001)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    datas = [{
        'text_col0': 'kiki-001',
        'text_col1': 'kiki',
        'n_col3': 25
    }, {
        'text_col0': 'goog-001',
        'text_col1': 'gogo',
        'n_col3': 101
    }]
    where1 = [{
        md.KEY_FIELDS_ID: 1346630691940601856
    }, {
        md.KEY_FIELDS_ID: 1346627944767950848
    }]
    wh1 = {
        # '#_id': 1346627944767950848
    }
    entity_id = 30004

    re = md.insert_execute(user_id, tenant_id, entity_id, datas)
    assert re is not None
    re = md.update_execute(user_id, tenant_id, entity_id, datas, where1)
    assert re is not None
    re = md.delete_execute(user_id, tenant_id, entity_id, where1)
    assert re is not None
    re = md.query_execute(user_id, tenant_id, entity_id, wh1)
    assert re is not None


def test_metadata_initial():
    # [{"entity_code":"table_name"}]
    entity_list = [{"entity_code": "Contract", "table_name": "data_t"}, {"entity_code": "BoQ", "table_name": "data_t"},
                   {"entity_code": "PU", "table_name": "data_t"}]
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    re = mdi.initialize_md_entities_from_tables(user_id, tenant_id, entity_list)
    logger.info("query all tables ,re={}".format(re))
    assert re is not None


def test_view():
    ## 业务数据测试data Test
    # # in(%s)
    # param = {"name1": ['abc', 'bb'], "name2": 'dfd33'}
    # # between %s and %s
    param = {"name1::1": 'abc', "name1::2": 'bb', "name2": 'dfd33'}
    user = ur.get_user("test1")
    qr = dv.query_view(user["user_id"], 50001, param)
    logger.info('view result:{}'.format(qr))
    assert qr is not None

    ## 元数据view测试
    param = {"teant_name_label": '%租户%', 'dept_name': '租户管理部门1'}
    user = ur.get_user("admin")
    qr = dv.query_view(user["user_id"], 50002, param)
    logger.info('view result:{}'.format(qr))
    assert qr is not None


# 从erwin反向生成表的元数据
def test_erwin_table_ini():
    user = ur.get_user("isales")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    schema = "SALE_LTC"
    database_name = "DG_EFINDB"
    # tables_list = ['roles']
    file_name = "D:\WorkDir\项目工作\合同中心\Contract_New202003.erwin"
    # file_name = "D:\WorkDir\Contract_New1.erwin"
    re = emg.reverse_tables_columns(user_id, tenant_id, database_name, schema, file_name)
    logger.info("all tables in[{}],re={}".format(schema, re))
    assert re is not None


# 从table生成默认ertity元数据
def test_entity_ini_from_tables():
    entity_list = [{"entity_code": "Contract", "table_name": "data_t"}, {"entity_code": "BoQ", "table_name": "data_t"}]
    user = ur.get_user("isales")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")

    # 从数据库反向工程，初始化表和字段元数据
    re = mdi.initialize_md_entities_from_tables(user_id, tenant_id, entity_list)
    return re


# 从erwin生成实体关系
def test_erwin_entity_relation_ini():
    user = ur.get_user("isales")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    schema = "SALE_LTC"
    database_name = "DG_EFINDB"
    # tables_list = ['roles']
    file_name = "D:\WorkDir\项目工作\合同中心\Contract_New202003.erwin"
    # erwin的外键关系转成元数据实体关系。
    re = emg.reverse_constraint(user_id, tenant_id, schema, file_name)
    logger.info("all rels in[{}],re={}".format(schema, re))
    assert re is not None


# 从元数据实体关系生成Neo4j图数据库
def test_entity_relation_2_neo4j():
    user = ur.get_user("isales")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    # Noe4j模型关系初始化
    entity_codes = None
    re = mdi.ini_entity_model_graph(tenant_id, entity_codes, 'entity_catagory', 'schema')
    logger.info("ini_entity_model_graph ,re={}".format(re))
    return re

# 插入默认字段
def test_entity_default_fields_insert():
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    # Noe4j模型关系初始化
    md_entity_ids = [1378186464011710464]
    entity_relative_tables_ids_list=[10003]
    re = md.insert_default_fields(user_id, tenant_id, md_entity_ids, entity_relative_tables_ids_list)
    logger.info("insert_default_fields ,re={}".format(re))
    return re

test_md()
test_view()
test_metadata_initial()
test_erwin_table_ini()
test_entity_ini_from_tables()
test_erwin_entity_relation_ini()
test_entity_relation_2_neo4j()
test_entity_default_fields_insert()
