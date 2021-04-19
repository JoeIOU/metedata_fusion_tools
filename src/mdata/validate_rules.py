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
rule_ui_template = """
        SELECT
            rr.rule_ui_rel_id,
            r.rule_id,
            rr.ui_template_id,
            rr.ui_fields_id,
            r.rule_code,
            r.rule_category,
            r.rule_type,
            r.rule_name,
            r.rule_script,
            r.rule_desc,
            r.rule_desc_en
        FROM
            rules r
        INNER JOIN rules_ui_rel rr ON rr.rule_id = r.rule_id
        AND rr.active_flag = 'Y'
        WHERE
            (
                r.tenant_id = %s
                OR r.public_flag = 'Y'
            )
        AND r.active_flag = 'Y'
        AND rr.ui_template_id = %s
        """


def get_rule_code_list(codes):
    code_list = []
    if codes is not None and len(codes) > 0:
        for item in codes:
            code = item.get("rule_code")
            if code is not None:
                code_list.append(code)
    return code_list


def get_rules(tenant_id, md_entity_id, rule_codes=None, n_rule_codes=None, validateOnly=False):
    sql = rule_sql
    new_rule_codes = None
    if validateOnly:
        sql += " AND r.rule_category='Validation'"
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


def get_rules_ui_template(tenant_id, ui_template_id, rule_codes=None):
    sql = rule_ui_template
    new_rule_codes = None
    if rule_codes is not None and len(rule_codes) > 0:
        sql += "  AND r.rule_code in %s"
        new_rule_codes = get_rule_code_list(rule_codes)
        pass

    conn = db_md()
    cursor = conn.cursor()
    if new_rule_codes is not None:
        cursor.execute(sql, args=(tenant_id, ui_template_id, new_rule_codes,))
    else:
        cursor.execute(sql, args=(tenant_id, ui_template_id,))
    result = cursor.fetchall()
    result = md.data_type_convert(result)
    logger.info("get_rules,result:{}".format(result))
    return result


def rule_field_mapping(rules, inputs):
    if rules is not None and inputs is not None:
        for item in rules:
            # field_name = item.get("md_fields_name")
            rule_code = item.get("rule_code")
            for item1 in inputs:
                rule_code1 = item1.get("rule_code")
                f_name = item1.get("field_name")
                if rule_code is not None and rule_code == rule_code1 and f_name is not None and len(f_name) > 0:
                    item["md_fields_name"] = f_name
                    break
    return rules


def validate_rules(rules, data):
    is_pass = True
    pass_list = []
    not_pass_list = []
    d_input = None
    reg = None
    item = None
    error_msg = None
    if data is None:
        logger.warning("validate_rules,data is None.")
    try:
        for item in rules:
            script = item.get("rule_script")
            # rule_code = item.get("rule_code")
            field_name = item.get("md_fields_name")
            rule_category = item.get("rule_category")
            type = item.get("rule_type")
            result = False
            output = None
            item['output'] = output
            item['result'] = result
            if data is not None and isinstance(data, list):
                if len(data) > 0:
                    data = data[0]
                else:
                    data = {}

            res = None
            # 1.正则表达式校验
            if type is not None and type.lower() == 'regex':
                d = None
                if isinstance(data, dict) and field_name is not None:
                    d = data.get(field_name)
                    if d is None:
                        d = ""
                        logger.warning("validate_rules,data is None by field={}.".format(field_name))
                else:
                    d = data
                reg = r'{}'.format(script)
                d_input = str(d)
                item['input'] = d_input
                if rule_category == 'Validation':  # 校验规则
                    res = rule.match(reg, d_input)
                else:
                    res = rule.search(reg, d_input)
                if res is not None:
                    result = True
                    output = res.group()
                else:
                    is_pass = False
                logger.info("validate_rules,rule=[{}],data:[{}],result:[{}]".format(reg, d, result))
            # 2.规则按公式计算
            elif type is not None and type.lower() == 'formula':
                reg = r'{}'.format(script)
                if field_name is None:
                    d_input = data
                    item['input'] = d_input
                    reg = reg % (d_input)
                else:
                    if isinstance(field_name, list):
                        tuple_field = ()
                        for key in field_name:
                            if isinstance(data, dict):
                                f = data.get(key)
                                tuple_field += (f,)
                        d_input = tuple_field
                        item['input'] = d_input
                        reg = reg % d_input
                    else:
                        d_input = data.get(field_name)
                        reg = reg % (d_input)
                item['input'] = d_input
                res = eval(reg)
                if res is not None:
                    result = True
                    output = res

            # 3.按脚本计算或判断
            elif type is not None and type.lower() == 'script':
                data_dict = data
                d_input = data_dict
                item['input'] = d_input
                exec(script, data_dict)
                result = data_dict.get("result")
                output = data_dict.get("output")
                if result is not None:
                    is_pass = False
            # 4.调用服务计算或判断
            else:
                pass

            item['input'] = d_input
            item['output'] = output
            item['result'] = result
            if result:
                pass_list.append(item)
            else:
                not_pass_list.append(item)

    except Exception as ex:
        error_msg = 'validate_rules exception,rule:%s,input:%s,message:%s' % (reg, d_input, ex)
        not_pass_list.append(item)
        logger.error(error_msg)
        is_pass = False
        # raise ex
    finally:
        return (is_pass, pass_list, not_pass_list, error_msg)


if __name__ == '__main__':
    # entity_ids = [30001, 30002, 30003]
    user = ur.get_user_tenant(1003)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    md_entity_id = 30015
    rules = [{'rule_code': 'rule_email'}]
    get_rules(tenant_id, md_entity_id, rules, None)
