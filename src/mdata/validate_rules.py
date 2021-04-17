# #####规则校验validate_rules.py
import re as rule
from db.db_conn import db_connection_metedata as db_md
from config.config import cfg as config
from mdata import metadata as md
from privilege import user_mngt as ur

logger = config.logger

rule_sql = """
        SELECT
            r.rule_id,
            e.md_entity_id,
            e.md_entity_code,
            e.md_entity_name,
            e.md_entity_name_en,
            f.md_fields_id,
            f.md_fields_name,
            f.md_fields_name_cn,
            f.md_fields_name_en,
            r.rule_code,
            r.rule_category,
            r.rule_type,
            r.rule_name,
            r.rule_script,
            r.rule_desc,
            r.rule_desc_en
        FROM
            rules r
        INNER JOIN rules_entity_rel rr ON rr.rule_id = r.rule_id
        AND rr.active_flag = 'Y'
        INNER JOIN md_entities e ON e.md_entity_id = rr.md_entity_id
        LEFT JOIN md_fields f ON f.md_fields_id = rr.md_fields_id
        WHERE
            (
                r.tenant_id = %s
                OR r.public_flag = 'Y'
            )
        AND r.active_flag = 'Y' 
        AND e.md_entity_id = %s
        """


def get_rule_code_list(codes):
    code_list = []
    if codes is not None and len(codes) > 0:
        for item in codes:
            code = item.get("rule_code")
            if code is not None:
                code_list.append(code)
    return code_list


def get_rules(tenant_id, md_entity_id, rule_codes=None, n_rule_codes=None):
    sql = rule_sql
    new_rule_codes = None
    if rule_codes is not None and len(rule_codes) > 0:
        sql += "  AND r.rule_code in %s"
        new_rule_codes = get_rule_code_list(rule_codes)
        pass
    elif n_rule_codes is not None and len(n_rule_codes) > 0:
        sql += "  AND r.rule_code not in %s"
        new_rule_codes = get_rule_code_list(n_rule_codes)
        pass

    conn = db_md()
    cursor = conn.cursor()
    if new_rule_codes is not None:
        cursor.execute(sql, args=(tenant_id, md_entity_id, new_rule_codes,))
    else:
        cursor.execute(sql, args=(tenant_id, md_entity_id,))
    result = cursor.fetchall()
    result = md.data_type_convert(result)
    logger.info("get_rules,result:{}".format(result))
    return result


def validate_rules(rules, data):
    is_pass = True
    pass_list = []
    not_pass_list = []
    for item in rules:
        script = item.get("rule_script")
        # rule_code = item.get("rule_code")
        field_name = item.get("md_fields_name")
        d = None
        if data is not None:
            if isinstance(data, dict) and field_name is not None:
                d = data.get(field_name)
            else:
                d = data
        # desc = item.get("rule_desc")
        rule_category = item.get("rule_category")
        type = item.get("rule_type")
        result = False
        output = None
        d_str = None
        if d is None:
            logger.warning("validate_rules,data is None.")
        else:
            if type and type.lower() == 'regex':  # 正则表达式
                res = None
                reg = r'{}'.format(script)
                d_str = str(d)
                if rule_category == 'Validation':  # 校验规则
                    res = rule.match(reg, d_str)
                else:
                    res = rule.search(reg, d_str)
                if res is not None:
                    result = True
                    output = res.group()
                else:
                    is_pass = False
                logger.info("validate_rules,rule=[{}],data:[{}],result:[{}]".format(reg, d, result))
            elif type and type.lower() == 'script':
                data_dict = data
                exec(script, data_dict)
                result = data_dict.get("result")
                if result is not None:
                    is_pass = False
            else:
                # service invoke
                pass
        item['input'] = d_str
        item['output'] = output
        item['result'] = result
        if result:
            pass_list.append(item)
        else:
            not_pass_list.append(item)

    return (is_pass, pass_list, not_pass_list)


if __name__ == '__main__':
    # entity_ids = [30001, 30002, 30003]
    user = ur.get_user_tenant(1003)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    md_entity_id = 30015
    rules = [{'rule_code': 'rule_email'}]
    get_rules(tenant_id, md_entity_id, rules, None)
