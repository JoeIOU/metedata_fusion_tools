
# ####util.py
# 通用工具和方法

# 根据符号，产生sql语句的格式
def gen_condition_sql(sign):
    re = ''
    if sign is None or len(sign) <= 0:
        sign = '='
    # param = '{' + param + '}'
    if sign == '=' or sign == '>' or sign == '<' or sign == '<=' or sign == '>=':
        re = sign + '%s'
    elif sign.upper() == 'between'.upper():
        re = ' between %s and %s'
    elif sign.upper() == 'like'.upper():
        re = ' like %s'
    elif sign == '!':
        re = '!=%s'
    elif sign.upper() == 'in'.upper():
        re = ' in %s '
    elif sign.upper() == 'not in'.upper():
        re = ' not in %s '
    elif sign.upper() == 'exists'.upper():
        re = ' exists (%s) '
    else:
        re = '=%s'

    return re
