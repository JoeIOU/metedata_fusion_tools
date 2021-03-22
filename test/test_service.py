# ######test_service.py
import requests

domain_url = "http://127.0.0.1:8888"


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
    return "success"


# ============================insert===================================
def md_insert():
    url = domain_url + "/services/insertEntity"

    payload = "{\"$_ENTITY_ID\":30001,\"data\":[{\"test_fields\":\"Mark\",\"test_fields1\":\"Mark0001\"}]}"
    headers = {
        'Authorization': 'Basic dGVzdDE6MTExMQ==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return "success"


def md_query():
    # ================================update===============================
    url = domain_url + "/md/services/findEntity?id=1346641783622340609&md_entity_id=30001"
    payload = {}
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def md_update():
    url = domain_url + "/md/services/updateEntity"

    payload = "{\"$_ENTITY_ID\":30047,\"data\":[{\"text_value\":1233444},{\"text_value\":\"test02\"}],\"where\":[{\"index_text_id\":1348844049557229568},{\"index_text_id\":1348892817107324928}]}"
    headers = {
        'Authorization': 'Basic dGVzdDE6MTExMTE=',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return "success"


def md_delete():
    url = domain_url + "/md/services/deleteEntity"

    payload = "{\"$_ENTITY_ID\":30047,\"where\":[{\"index_text_id\":1348844049557229568}]}"
    headers = {
        'Authorization': 'Basic dGVzdDE6MTExMQ==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFMgnQ.g1_9KHHCIyu-2yHAIq6-YB7hZms'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return "success"


def view_query():
    url = domain_url + "/md/services/queryView"

    payload = "{\"view_id\":50001,\"name002\": [\"abc\", \"bb\"], \"name2\": \"dfd33\"}"
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def findEntitySetup():
    url = domain_url + "/services/findEntitySetup?$_ENTITY_ID=30047"

    payload = {}
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def queryEntityByCodeOrID():
    url = domain_url + "/services/queryEntityByCodeOrID?$_ENTITY_CODE=md_entities&$_ENTITY_ID=30015"
    payload = {}
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def queryFieldsByCodeOrID():
    url = domain_url + "/services/queryFieldsByCodeOrID?$_ENTITY_CODE=md_fields&$_ENTITY_ID=30015"
    payload = {}
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def findTableByName():
    url = domain_url + "/services/findTableByName?table_names=data_t"

    payload = "{\"table_names\":[\"abc\"]}"
    headers = {
        'Authorization': 'Basic dGVzdDE6MTIzNDU=',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokolaQWlxgq6QDpvESgeGaKkpWhDlg5hG1gAOPmJeamQjXEgwQMlWqhMlBDkUzDpQEAom8vAA.YFg4Tg.iGELYRQIg8g_2IgmiGVwVkA-_XY'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    return "success"


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
    re = queryEntityByCodeOrID()
    assert re == "success"
    re = findTableByName()
    assert re == "success"


test_dm()
