# #####ui_metadata.py,UI元数据配置
from config.config import cfg as config
from privilege import user_mngt as ur
from db.db_conn import db_connection_metedata as db_md

logger = config.logger

sql_ui_entity_single = """
        SELECT
            r.ui_entity_rel_id,
            r.entity_sequence,
            r.entity_id,
            r.ui_entity_rel_desc,
            e.md_entity_code,
            e.md_entity_name,
            e.md_entity_name_en,
            f.ui_fields_id,
            f.ui_fields_name_cn,
            f.ui_fields_name_en,
            f.ui_fields_type,
            f.linked_field_id,
            f.field_sequence,
            f.text_column1 message_key,
            ff.md_fields_id,
            ff.md_fields_name
        FROM
            ui_entity_rel r
        INNER JOIN md_entities e ON r.entity_id = e.md_entity_id
        AND e.active_flag = 'Y'
        LEFT JOIN ui_fields f ON r.ui_entity_rel_id = f.ui_entity_rel_id
        AND f.active_flag = 'Y'
        LEFT JOIN md_fields ff ON ff.md_fields_id = f.md_field_id
        AND ff.active_flag = 'Y'
        AND ff.md_entity_id = e.md_entity_id
        WHERE
            (
                e.tenant_id = %s
                OR e.public_flag = 'Y'
            )
        AND r.active_flag = 'Y'
        AND r.ui_template_id is NULL
        AND r.entity_id = %s
"""

sql_ui_entity_by_template = """
        SELECT t.ui_template_id,
            t.ui_template_code,
            t.ui_template_type,
            t.ui_template_model,
            t.ui_template_name,
            r.ui_entity_rel_id,
            r.entity_sequence,
            r.entity_id,
            r.parent_entity_id,
            r.ui_entity_rel_desc,
            e.md_entity_code,
            e.md_entity_name,
            e.md_entity_name_en
        FROM
            ui_entity_rel r
        INNER JOIN ui_template t ON r.ui_template_id = t.ui_template_id
        AND t.active_flag = 'Y'
        INNER JOIN md_entities e ON r.entity_id = e.md_entity_id
        AND e.active_flag = 'Y'
        WHERE
            (
                e.tenant_id = %s
                OR e.public_flag = 'Y'
            )
        AND r.active_flag = 'Y'
"""

sql_ui_entity_fields_by_template = """
        SELECT t.ui_template_id,
            t.ui_template_code,
            t.ui_template_type,
            t.ui_template_model,
            t.ui_template_name,
            r.ui_entity_rel_id,
            r.entity_sequence,
            r.entity_id,
            r.parent_entity_id,
            r.ui_entity_rel_desc,
            e.md_entity_code,
            e.md_entity_name,
            e.md_entity_name_en,
            f.ui_fields_id,
            f.ui_fields_name_cn,
            f.ui_fields_name_en,
            f.ui_fields_type,
            f.linked_field_id,
            f.field_sequence,
            f.text_column1 message_key,
            ff.md_fields_id,
            ff.md_fields_name
        FROM
            ui_entity_rel r
        INNER JOIN ui_template t ON r.ui_template_id = t.ui_template_id
        AND t.active_flag = 'Y'
        INNER JOIN md_entities e ON r.entity_id = e.md_entity_id
        AND e.active_flag = 'Y'
        INNER JOIN ui_fields f ON r.ui_entity_rel_id = f.ui_entity_rel_id
        AND f.active_flag = 'Y'
        INNER JOIN md_fields ff ON ff.md_fields_id = f.md_field_id
        AND ff.active_flag = 'Y'
        WHERE
            (
                e.tenant_id = %s
                OR e.public_flag = 'Y'
            )
        AND r.active_flag = 'Y'
"""

# 不带模板的单个实体对象的ui对象和属性查询
def query_single_ui_entity_elements(tenant_id, entity_id):
    sql = sql_ui_entity_single
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=(tenant_id, entity_id,))
    result = cursor.fetchall()
    logger.info("query_single_ui_entity_elements:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result

# 带模板的ui对象查询
def query_ui_entity_by_template(tenant_id, entity_id, ui_template_id, ui_template_code=None):
    sql = sql_ui_entity_by_template
    args = (tenant_id,)
    if (ui_template_id is None and ui_template_code is None):
        logger.warning("ui_template_id nad ui_template_code is Null.")
        return None
    if (ui_template_id is not None):
        sql += " AND t.ui_template_id =%s"
        args += (ui_template_id,)
    elif ui_template_code is not None:
        sql += " AND t.ui_template_code =%s"
        args += (ui_template_code,)

    if (entity_id is not None):
        sql += " AND r.entity_id = %s"
        args += (entity_id,)

    sql+=" order by r.entity_sequence,r.entity_id"
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=args)
    result = cursor.fetchall()
    logger.info("query_ui_entity_by_template:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result

# 带模板的ui对象和属性查询
def query_ui_entity_fields_by_template(tenant_id, entity_id, ui_template_id, ui_template_code=None):
    sql = sql_ui_entity_fields_by_template
    args = (tenant_id,)
    if (ui_template_id is None and ui_template_code is None):
        logger.warning("ui_template_id nad ui_template_code is Null.")
        return None
    if (ui_template_id is not None):
        sql += " AND t.ui_template_id =%s"
        args += (ui_template_id,)
    elif ui_template_code is not None:
        sql += " AND t.ui_template_code =%s"
        args += (ui_template_code,)

    if (entity_id is not None):
        sql += " AND r.entity_id = %s"
        args += (entity_id,)

    sql+=" order by r.entity_sequence,r.entity_id,f.field_sequence"
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=args)
    result = cursor.fetchall()
    logger.info("query_ui_entity_fields_by_template:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result

if __name__ == '__main__':
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    ui_template_id = 1384807373854294016
    ui_template_code = "ui_template_001"
    entity_id = 30016
    res = query_single_ui_entity_elements(tenant_id, entity_id)
    entity_id = 30015
    res = query_ui_entity_fields_by_template(tenant_id, entity_id, ui_template_id, )
    res = query_ui_entity_fields_by_template(tenant_id, None, None, ui_template_code)
    pass
