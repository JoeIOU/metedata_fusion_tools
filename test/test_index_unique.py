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
