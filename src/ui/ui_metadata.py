# #####ui_metadata.py,UI元数据配置
from config.config import cfg as config
from privilege import user_mngt as ur
from db.db_conn import db_connection_metedata as db_md

logger = config.logger

sql_ui = """
        SELECT
            t.ui_template_id,
            t.ui_template_type,
            t.ui_template_model,
            t.ui_template_name,
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
            f.linked_field_id
        FROM
            ui_template t
        INNER JOIN ui_entity_rel r ON r.ui_template_id = t.ui_template_id
        AND r.active_flag = 'Y'
        LEFT JOIN md_entities e ON r.entity_id = e.md_entity_id
        AND e.active_flag = 'Y'
        LEFT JOIN ui_fields f ON r.ui_entity_rel_id = f.ui_entity_rel_id
        AND f.active_flag = 'Y'
        WHERE
            (
                t.tenant_id = %s
                OR t.public_flag = 'Y'
            )
        AND t.active_flag = 'Y'
        AND t.ui_template_id = %s
"""

sql_ui_entity = """
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
            ff.md_fields_id,
            ff.md_fields_name,
            f.linked_field_id,
            f.text_column1 message_key
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


def query_ui_template_elements(tenant_id, ui_template_id):
    sql = sql_ui
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=(tenant_id, ui_template_id,))
    result = cursor.fetchall()
    logger.info("query_ui_template_elements:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


def query_single_ui_entity_elements(tenant_id, entity_id):
    sql = sql_ui_entity
    conn = db_md()
    cursor = conn.cursor()
    cursor.execute(sql, args=(tenant_id, entity_id,))
    result = cursor.fetchall()
    logger.info("query_single_ui_entity_elements:{}".format(result))
    conn.close()  # 不是真正关闭，而是重新放回了连接池
    return result


if __name__ == '__main__':
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    ui_template_id = 1384807373854294016
    re = query_ui_template_elements(tenant_id, ui_template_id)
    entity_id = 30016
    res = query_single_ui_entity_elements(tenant_id, entity_id)
    pass
