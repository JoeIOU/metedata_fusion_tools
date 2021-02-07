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
