# #####规则校验validate_rules.py
import re as rule
from db.db_conn import db_connection_metedata as db_md
from config.config import cfg as config
from mdata import metadata as md
from privilege import user_mngt as ur

logger = config.logger

rule_sql = """
        SELECT
            e.md_entity_id,
            e.md_entity_code,
            e.md_entity_name,
            e.md_entity_name_en,
            rr.rule_entity_rel_id,
            rr.input_params,
            rr.output_params,
            r.rule_id,
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
        WHERE
            (
                r.tenant_id = %s
                OR r.public_flag = 'Y'
            )
        AND r.active_flag = 'Y' 
        AND e.md_entity_id = %s
        """
rule_entity_sql = """
        SELECT
            rr.rule_entity_rel_id,
            r.rule_id,
            rr.md_entity_id,
            rr.input_params,
            rr.output_params,
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
        WHERE
            (
                r.tenant_id = %s
                OR r.public_flag = 'Y'
            )
        AND r.active_flag = 'Y'
        AND rr.md_entity_id = %s
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


def get_rules(tenant_id, md_entity_id, rule_codes=None, n_rule_codes=None, validateOnly=0):
    sql = rule_sql
    new_rule_codes = None
    if validateOnly == 1:
        sql += " AND r.rule_category='Validation'"
    elif validateOnly == 2:
        sql += " AND r.rule_category='Computing'"
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


def get_rules_entity(tenant_id, md_entity_id, rule_category, rule_codes=None):
    sql = rule_entity_sql
    new_rule_codes = None
    if rule_codes is not None and len(rule_codes) > 0:
        new_rule_codes = get_rule_code_list(rule_codes)
        if new_rule_codes is not None:
            sql += "  AND r.rule_code in %s"
    if rule_category is not None:
        sql += "  AND r.rule_category = %s"
        pass

    conn = db_md()
    cursor = conn.cursor()
    args = (tenant_id, md_entity_id,)
    if new_rule_codes is not None:
        args += (new_rule_codes,)
    if rule_category is not None:
        args += (rule_category,)
    cursor.execute(sql, args=args)
    result = cursor.fetchall()
    result = md.data_type_convert(result)
    logger.info("get_rules_entity,result:{}".format(result))
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
    logger.info("get_rules_ui_template,result:{}".format(result))
    return result


def rule_field_mapping(rules, inputs):
    if rules is not None and inputs is not None:
        for item in rules:
            rule_code = item.get("rule_code")
            for item1 in inputs:
                rule_code1 = item1.get("rule_code")
                input_params = item1.get("input_params")
                output_params = item1.get("output_params")
                if rule_code is not None and rule_code == rule_code1:
                    if input_params is not None and len(
                            input_params) > 0:
                        item["input_params"] = input_params
                    if output_params is not None and len(
                            output_params) > 0:
                        item["output_params"] = output_params
                    break
    return rules


def validate_rules(rules, data):
    is_pass = True
    pass_list = []
    not_pass_list = []
    output_data = {}
    d_input = None
    reg = None
    item = None
    error_msg = None
    try:
        if data is None or not isinstance(data, dict):
            logger.warning("validate_rules,data is None.")
            is_pass = False
            error_msg = '输入校验数据{}，为空或不是对象，请修改确认后，再重新执行。'.format(data)
        else:
            for item in rules:
                script = item.get("rule_script")
                # rule_code = item.get("rule_code")
                input_params = item.get("input_params")
                if input_params is not None and isinstance(input_params, str) and input_params.find(
                        "[") >= 0 and input_params.find("]") >= 0:
                    input_params = eval(input_params)
                output_params = item.get("output_params")
                if output_params is not None and isinstance(output_params, str) and output_params.find(
                        "[") >= 0 and output_params.find("]") >= 0:
                    output_params = eval(output_params)
                rule_category = item.get("rule_category")
                type = item.get("rule_type")
                result = False
                output = None
                item['$rule_output'] = output
                item['$rule_result'] = result
                if data is not None and isinstance(data, list):
                    if len(data) > 0:
                        data = data[0]
                    else:
                        data = {}

                res = None
                message = None
                # 1.正则表达式校验
                if type is not None and type.lower() == 'regex':
                    d = None
                    if isinstance(data, dict) and input_params is not None:
                        field_name = None
                        if isinstance(input_params, list) and len(input_params) > 0:
                            field_name = str(input_params[0])
                        else:
                            field_name = input_params
                        d = data.get(field_name)
                        if d is None:
                            logger.warning("validate_rules,data is None by field={}.".format(field_name))
                            message = "输入参数[{}]，在输入校验数据中，没有找到对应的参数值。".format(field_name)
                            item['$message'] = message
                    else:
                        d = data
                    reg = r'{}'.format(script)
                    item['$rule_input'] = d
                    # if d is None:
                    #     d = ""
                    d_input = d
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
                    if input_params is None:
                        d_input = data
                        item['$rule_input'] = d_input
                        reg = reg % (d_input)
                    else:
                        if isinstance(input_params, list) and len(input_params) > 0:
                            tuple_field = ()
                            for key in input_params:
                                if isinstance(data, dict):
                                    f = data.get(key)
                                    tuple_field += (f,)
                            d_input = tuple_field
                            item['$rule_input'] = d_input
                            reg = reg % d_input
                        else:
                            d_input = data.get(str(input_params))
                            reg = reg % (d_input)
                    item['$rule_input'] = d_input
                    res = eval(reg)
                    if res is not None:
                        result = True
                        output = res

                # 3.按脚本计算或判断
                elif type is not None and type.lower() == 'script':
                    data_dict = data
                    d_input = data_dict
                    item['$rule_input'] = d_input
                    exec(script, data_dict)
                    result = data_dict.get("result")
                    output = data_dict.get("$rule_output")
                    if result is not None:
                        is_pass = False
                # 4.调用服务计算或判断
                else:
                    pass

                item['$rule_input'] = d_input
                item['$rule_output'] = output
                if message is not None:
                    item['$message'] = message
                if output_params is not None:
                    key = None
                    if isinstance(output_params, list) and len(output_params) > 0:
                        key = output_params[0]
                    else:
                        key = str(output_params)
                    output_data[key] = output
                    if rule_category == 'Validation':
                        output_data[key] = result

                item['$rule_result'] = result
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
        logger.info("output Data:{}".format(output_data))
        return (is_pass, pass_list, not_pass_list, output_data, error_msg)


if __name__ == '__main__':
    # entity_ids = [30001, 30002, 30003]
    user = ur.get_user_tenant(1003)
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    md_entity_id = 30015
    rules = [{'rule_code': 'rule_email'}]
    get_rules(tenant_id, md_entity_id, rules, None)
