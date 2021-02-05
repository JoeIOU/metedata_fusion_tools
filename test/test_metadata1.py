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

def test_erwin_ini():
    user = ur.get_user("isales")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    schema = "SALE_LTC"
    database_name = "DG_EFINDB"
    # tables_list = ['roles']
    file_name = "D:\WorkDir\项目工作\合同中心\Contract_New202003.erwin"
    # file_name = "D:\WorkDir\Contract_New1.erwin"
    re = emg.reverse_tables_columns(user_id, tenant_id, database_name, schema, file_name)
    assert re is not None
    logger.info("all tables in[{}],re={}".format(schema, re))


    # erwin的外键关系转成元数据实体关系。
    # re = emg.reverse_constraint(user_id, tenant_id, schema, file_name)
    # logger.info("all rels in[{}],re={}".format(schema, re))
    # assert re is not None



test_md()
test_view()
test_metadata_initial()
test_erwin_ini()
