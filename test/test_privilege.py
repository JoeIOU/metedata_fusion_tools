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
