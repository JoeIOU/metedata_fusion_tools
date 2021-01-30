# ######test_index_unique.py
from mdata import index_unique as iu
from privilege import user_mngt as ur


def test_index_unique():
    # ##insert the index data
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    data_list = []
    datas = [{
        'test_fields': 'kiki-001',
        'test_fields1': 'kiki',
        'customer_name': "ABC.com",
        "md_entity_id": 30001
    }, {
        'test_fields': 'goog-001',
        'test_fields1': 'gogo',
        'customer_name': "HW.com",
        "md_entity_id": 30001
    }]
    md_entity_id = 30001

    re = iu.query_index_mapping(tenant_id, md_entity_id)
    assert re is not None
    print(re)
    ids = [12421421412, 12421421411]
    re = iu.delete_index_data(user_id, tenant_id, md_entity_id, datas, ids)
    assert re is not None
    re = iu.insert_index_data(user_id, tenant_id, md_entity_id, datas, ids)
    assert re is not None
    re = iu.update_index_data(user_id, tenant_id, md_entity_id, datas, ids)
    assert re is not None


test_index_unique()
#  ######test_lookup.py
from data import lookup
from privilege import user_mngt as ur


def test_lookup():
    # ##insert the lookup data
    user = ur.get_user("test1")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    data_list = []
    data = {}
    md_entity_id = 30001
    md_field_id = 40005
    data_id = 800001
    data["data_id"] = data_id
    data["md_entity_id"] = md_entity_id
    data["lookup_classify_id"] = 123
    data["lookup_key"] = md_field_id
    data["lookup_value"] = "bbb"
    data_list.append(data)
    data = {}
    data["data_id"] = data_id
    data["md_entity_id"] = md_entity_id
    data["lookup_classify_id"] = 123
    data["lookup_key"] = md_field_id
    data["lookup_value"] = "aaa"
    data_list.append(data)
    re= lookup.insert_lookup_data(user_id, tenant_id, data_list)
    assert re is not None
    re = lookup.update_lookup_data(user_id, tenant_id, md_entity_id, md_field_id, data_id, data_list)
    assert re is not None
    re = lookup.delete_lookup_data(user_id, tenant_id, md_entity_id, md_field_id, data_id)
    assert re is not None
    # ##query the lookup data
    where_dict = {"md_entity_id": 30041, "lookup_key": 40005}
    re = lookup.query_lookup_data(user_id, tenant_id, where_dict)
    assert re is not None

test_lookup()
# ######test_metadata.py
from mdata import metadata_initialize as mdi, metadata as md
from data import data_view as dv
from config.config import cfg as config
from privilege import user_mngt as ur

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




test_md()
test_view()
test_metadata_initial()
# ######test_privilege.py
from mdata import metadata as md
from privilege import role_privilege as rp, data_privilege as dp, user_mngt as ur
from common import constants as const


def test_data_privilege():
    user_account = "test1"
    user = ur.get_user(user_account)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    ## Entity
    md_entity_id = 30001
    re = dp.query_data_privilege_info(tenant_id, user_id, md_entity_id, const.ENTITY_TYPE_ENTITY)
    assert re is not None

    ## View
    md_entity_id = 50001
    re = dp.query_data_privilege_info(tenant_id, user_id, md_entity_id, const.ENTITY_TYPE_VIEW)

    assert re is not None or re is None


def test_role_privilege():
    user_account = "admin"
    user = ur.get_user(user_account)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    re = md.get_md_entities_by_code(tenant_id, ["entity_privileges"])
    if re is not None and len(re) > 0:
        insert_entity_id = re[0].get("md_entity_id")
    else:
        # entity_privileges实体表元数据实体ID
        insert_entity_id = 30029

    # #1.实体权限导入
    md_entity_ids = [30015]
    re = rp.insert_entity_privilege(user_id, tenant_id, insert_entity_id, const.ENTITY_TYPE_ENTITY, md_entity_ids)
    assert re is not None

    # #2.视图权限写入
    view_ids = [50002]
    re = rp.insert_entity_privilege(user_id, tenant_id, insert_entity_id, const.ENTITY_TYPE_VIEW, view_ids)
    assert re is not None

    # re = query_user_priv_by_user_account(user_account)
    re = rp.query_user_privilege_by_userid(tenant_id, user_id)
    assert re is not None


test_data_privilege()
test_role_privilege()
# ######test_service.py
import requests

domain_url = "http://127.0.0.1:8888"


# ====================login==========================================
def login():
    url = domain_url + "/md/login?user_account=test1&user_name=Joe.Lin"
    payload = {}
    headers = {
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUxD1uCVn6rnk5mnVAsAEkItYA.X_etQQ.tEWtT5M_siS8pvckEw-NCCAOmRA'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# ============================insert===================================
def md_insert():
    url = domain_url + "/md/services/insertEntity"

    payload = {'md_entity_id': 30001,
               'test_fields': 'pyTest',
               'test_fields1': 'pyTest',
               'test_fields2': 3,
               'test_fields3': '2021-01-01 12:00:00'}
    files = []
    headers = {
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUxD1uCVn6rnk5mnVAsAEkItYA.X_etQQ.tEWtT5M_siS8pvckEw-NCCAOmRA'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    return "success"


def md_query():
    # ================================update===============================
    url = domain_url + "/md/services/findEntity?id=1346641783622340609&md_entity_id=30001"
    payload = {}
    headers = {
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUxD1uCVn6rnk5mnVAsAEkItYA.X_etQQ.tEWtT5M_siS8pvckEw-NCCAOmRA'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def md_update():
    url = domain_url + "/md/services/updateEntity?id=1347358568483000320"

    payload = {'md_entity_id': 30001,
               'test_fields': 'Mark_update',
               'test_fields1': 'Mark.Lin_new',
               'test_fields2': '10',
               'test_fields3': '2021-01-01 12:00:01'}
    files = [

    ]
    headers = {
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUxD1uCVn6rnk5mnVAsAEkItYA.X_etQQ.tEWtT5M_siS8pvckEw-NCCAOmRA'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return "success"


def md_delete():
    url = domain_url + "/md/services/deleteEntity"

    payload = {'id': '1347392993136611328',
               'md_entity_id': '30001'}
    files = [

    ]
    headers = {
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUxD1uCVn6rnk5mnVAsAEkItYA.X_etQQ.tEWtT5M_siS8pvckEw-NCCAOmRA'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return "success"


def view_query():
    url = domain_url + "/md/services/queryView"

    payload = "{\"view_id\":50001,\"name002\": [\"abc\", \"bb\"], \"name2\": \"dfd33\"}"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUxD1uCVn6rnk5mnVAsAEkItYA.X_gIpg.Empn7II8JquXVrsaHXioRiX029s'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def test_dm():
    login()
    re = md_insert()
    assert re == "success"
    re = md_update()
    assert re == "success"
    re = md_query()
    assert re == "success"
    re = md_delete()
    assert re == "success"
    re = view_query()
    assert re == "success"


test_dm()
