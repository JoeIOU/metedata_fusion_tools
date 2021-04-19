# ######test_service.py
import requests
import json

domain_url = "http://127.0.0.1:8888/md"
auth_token = 'Basic dGVzdDE6MTIzNDU='


# ====================login==========================================
def login():
    url = domain_url + "/login"

    payload = {'username': 'test1',
               'password': '121212'}
    files = [

    ]
    headers = {
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


# ============================insert===================================
def md_insert():
    url = domain_url + "/services/insertEntity"

    payload = "{\"$_ENTITY_ID\":30001,\"data\":[{\"test_fields\":\"Mark\",\"test_fields1\":\"Mark0001\"}]}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def md_query():
    # ================================update===============================
    url = domain_url + "/services/findEntity?$_ENTITY_ID=30015&md_entity_id=1373928231974211584"

    payload = "{\"$_ENTITY_ID\":30015,\"where\":[{\"md_entity_id\":1373928231974211584},{\"md_entity_id\":1348892817107324928}]}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFwHUA.D3nKN48L6EIW5TvEAbOJB4ZFMzM'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def md_update():
    url = domain_url + "/services/updateEntity"

    payload = "{\"$_ENTITY_ID\":30001,\"data\":[{\"test_fields\":\"12323\"},{\"test_fields\":\"test02\"}],\"where\":[{\"id\":1348844049557229568},{\"id\":1348892817107324928}]}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def md_delete():
    url = domain_url + "/services/deleteEntity"

    payload = "{\"$_ENTITY_ID\":30001,\"where\":[{\"id\":1348844049557229568}]}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def view_query():
    url = domain_url + "/services/queryView?$_VIEW_ID=50001"

    payload = "{\"$_VIEW_ID\":30001,\"name002\": [\"abc\", \"bb\"], \"name2\": \"dfd33\"}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YF1MSg.qMO8j0nSj6VwvEJ0AxpgfYjIAJ0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        # print(data.get("message").decode("utf-8"))
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def queryEntityList():
    url = domain_url + "/services/queryEntityList"

    payload = {}
    headers = {
        'Authorization': auth_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def findEntitySetup():
    url = domain_url + "/services/findEntitySetup?$_ENTITY_ID=30047"

    payload = {}
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def queryEntityByCodeOrID():
    url = domain_url + "/services/queryEntityByCodeOrID?$_ENTITY_CODE=md_entities&$_ENTITY_ID=30015"
    payload = {}
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def queryFieldsByCodeOrID():
    url = domain_url + "/services/queryFieldsByCodeOrID?$_ENTITY_CODE=md_fields&$_ENTITY_ID=30015"
    payload = {}
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def findTableByName():
    url = domain_url + "/services/findTableByName?table_names=data_t"

    payload = "{\"table_names\":[\"abc\"]}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFg4Tg.iGELYRQIg8g_2IgmiGVwVkA-_XY'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def findLookupByEntityCode():
    url = domain_url + "/services/findLookupByEntityCode?entity_code=lookup_classify&lookup_code="

    payload = {}
    headers = {
        'Authorization': auth_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def validateRules():
    url = domain_url + "/services/validateRules?rule_code=rule_email&$_ENTITY_ID=30015&data=abc@hhcp.com"

    payload = "{\"$_ENTITY_ID\":30015,\r\n\"rules\":[{\"rule_code\":\"rule_alphabet_underline\"},{\"rule_code\":\"rule_discount_amount_calc\",\"field_name\":[\"x\",\"y\"]}],\r\n\"n_rules\":[{\"rule_code\":\"rule_discount_amount_calc\"}],\r\n\"data\":{\"md_entity_code\":\"branchs\",\"x\":200,\"y\":5}\r\n}"
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    status = None
    if response is not None:
        data = json.loads(response.text)
        status = data.get("status")
    if status is not None and status < 300:
        return "success"
    else:
        return None


def test_dm():
    login()
    re = md_insert()
    assert re == "success"
    re = md_update()
    assert re == "success"
    re = md_query()
    assert re == "success"
    re = md_delete()
    assert re == "success"
    re = view_query()
    assert re == "success"
    re = findEntitySetup()
    assert re == "success"
    re = queryEntityByCodeOrID()
    assert re == "success"
    re = queryFieldsByCodeOrID()
    assert re == "success"
    re = findTableByName()
    assert re == "success"
    re = queryEntityList()
    assert re == "success"
    re = findLookupByEntityCode()
    assert re == "success"
    re = validateRules()
    assert re == "success"


test_dm()
