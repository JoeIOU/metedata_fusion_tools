# ######lookup.py
# lookup多值或者选择其他实体，如客户、产品等
from mdata import metadata as md
from privilege import user_mngt as ur
from config.config import cfg as config

logger = config.logger

MD_LOOKUP_METADATA_ENTITY_NAME = "data_lookup_set"


def insert_lookup_data(user_id, tenant_id, data_list):
    rr = md.get_md_entities_id_by_code([MD_LOOKUP_METADATA_ENTITY_NAME])
    re = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
        if entity_id is not None:
            re = md.insert_execute(user_id, tenant_id, entity_id, data_list)
    if re is None:
        logger.warning(
            "insert_lookup_data,insert nothing,tables=[{}],data:{}.".format(MD_LOOKUP_METADATA_ENTITY_NAME, data_list))
    return re


def update_lookup_data(user_id, tenant_id, md_entity_id, md_field_id, data_id, data_list):
    rr = md.get_md_entities_id_by_code([MD_LOOKUP_METADATA_ENTITY_NAME])
    re = None
    entity_id = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
    if data_list is None or len(data_list) <= 0:
        return None
    md_dict = data_list[0]
    if entity_id is not None:
        where_list = []
        where_dict = {}
        where_dict["data_id"] = data_id
        where_dict["md_entity_id"] = md_entity_id
        where_dict["lookup_key"] = md_field_id
        where_list.append(where_dict)
        re = md.delete_execute(user_id, tenant_id, entity_id, where_list)
        re = md.insert_execute(user_id, tenant_id, entity_id, data_list)
    if re is None:
        logger.warning(
            "update_lookup_data,insert nothing,tables=[{}],data:{}.".format(MD_LOOKUP_METADATA_ENTITY_NAME, data_list))
    return re


def delete_lookup_data(user_id, tenant_id, md_entity_id, md_field_id, data_id):
    rr = md.get_md_entities_id_by_code([MD_LOOKUP_METADATA_ENTITY_NAME])
    re = None
    entity_id = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
    where_list = []
    if entity_id is not None:
        where_dict = {}
        where_dict["data_id"] = data_id
        where_dict["md_entity_id"] = md_entity_id
        where_dict["lookup_key"] = md_field_id
        where_list.append(where_dict)
        re = md.delete_execute(user_id, tenant_id, entity_id, where_list)
    if re is None:
        logger.warning(
            "delete_lookup_data,insert nothing,tables=[{}],data:{}.".format(MD_LOOKUP_METADATA_ENTITY_NAME, where_list))
    return re


def query_lookup_data(user_id, tenant_id, where_dict):
    rr = md.get_md_entities_id_by_code([MD_LOOKUP_METADATA_ENTITY_NAME])
    re = None
    if rr is not None and len(rr) > 0:
        entity_id = rr[0].get("md_entity_id")
        if entity_id is not None:
            re = md.query_execute(user_id, tenant_id, entity_id, where_dict)
    return re


if __name__ == '__main__':
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
    # insert_lookup_data(user_id, tenant_id,data_list)
    re = update_lookup_data(user_id, tenant_id, md_entity_id, md_field_id, data_id, data_list)
    # re = delete_lookup_data(user_id, tenant_id, md_entity_id, md_field_id, data_id)

    # ##query the lookup data
    where_dict = {"md_entity_id": 30041, "lookup_key": 40005}
    re1 = query_lookup_data(user_id, tenant_id, where_dict)
    logger.info("result:{}".format(re1))
