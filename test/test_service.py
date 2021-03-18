# ######test_service.py
import requests

domain_url = "http://127.0.0.1:8888"


# ====================login==========================================
def login():
    url = domain_url + "/md/login?user_account=test1&user_name=Joe.Lin"
    payload = {}
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# ============================insert===================================
def md_insert():
    url = domain_url + "/md/services/insertEntity"

    payload = {'md_entity_id': 30001,
               'test_fields': 'pyTest',
               'test_fields1': 'pyTest',
               'test_fields2': 3,
               'test_fields3': '2021-01-01 12:00:00'}
    files = []
    headers = {
      'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
      'Content-Type': 'application/json',
      'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
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
    url = domain_url + "/md/services/updateEntity?id=1347358568483000320"

    payload = {'md_entity_id': 30001,
               'test_fields': 'Mark_update',
               'test_fields1': 'Mark.Lin_new',
               'test_fields2': '10',
               'test_fields3': '2021-01-01 12:00:01'}
    files = [

    ]
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return "success"


def md_delete():
    url = domain_url + "/md/services/deleteEntity"

    payload = {'id': '1347392993136611328',
               'md_entity_id': '30001'}
    files = [

    ]
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

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
    url = "http://127.0.0.1:8888/md/services/findEntitySetup?$_ENTITY_ID=30047"

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
    url = "http://127.0.0.1:8888/md/services/queryEntityByCodeOrID?$_ENTITY_CODE=md_entities&$_ENTITY_ID=30015"
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
    url = "http://127.0.0.1:8888/md/services/queryFieldsByCodeOrID?$_ENTITY_CODE=md_fields&$_ENTITY_ID=30015"
    payload = {}
    headers = {
        'Authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWXhOVGszTURJM01Td2laWGh3SWpveE5qRTJNREEyTWpjeGZRLmV5SjFjMlZ5WDJsa0lqb2lZV1J0YVc0aWZRLjNKMkhTYXp5SGZseUVub3VEVEc3RW00UDJvWVRBaFVWU3BfT3pYcktoZVQ5dy1vc00tSGtFV2xTZWVWZmpCcU5tOElmTnZYUUY3Tmt5a3VFampMa0h3Og==',
        'Content-Type': 'application/json',
        'Cookie': 'session=.eJyrViotTi1SsqpWSkxOzi_NK4nPK81NAokoJabkZuYp6SiVpOYlAsUzU5SsDA0MdMAaYDxjKDcvMTcVrqUWKgg1EckoLGoBFxUrhg.YFG_3w.OPt6SlSWffEO4mgc3rmKJLH5HT4'
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


test_dm()
