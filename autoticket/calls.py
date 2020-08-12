import json

from autoticket import config
import requests

busObId = '6dd53665c0c24cab86870a21cf6434ae'


def gettoken():
    payload = {'grant_type': 'password',
               'client_id': config.clientID,
               'username': config.username,
               'password': config.password}

    header = {'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json'}

    return requests.post(config.url + 'token', data=payload, headers=header).json()['access_token']


def gettemplate():
    token = gettoken()

    auth_header = {'Accept': 'application/json',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Bearer ' + token}

    payload = {
        'busObId': busObId,
        'includeAll': 'true',
        'includeRequired': 'true'
    }

    return requests.post(config.url + 'api/V1/getbusinessobjecttemplate', data=payload, headers=auth_header).json()


def createticket(fields):
    token = gettoken()

    payload = {
        "busObId": busObId,
        "busObPublicId": "",
        "busObRecId": "",
        "cacheKey": "",
        "cacheScope": "Tenant",
        "fields": fields,
        "persist": True
    }

    auth_header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    # have default fields that havent been set
    return requests.post(config.url + 'api/V1/savebusinessobject', data=json.dumps(payload), headers=auth_header).json()


def getticket(publicid):
    token = gettoken()

    auth_header = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    return requests.get(config.url + '/api/V1/getbusinessobject/busobid/' + busObId + '/publicid/' + publicid,
                        headers=auth_header).json()


def addattachment(body, filename, publicid, totalsize):
    token = gettoken()

    auth_header = {
        'Accept': 'application/json',
        'Content-Type': 'application/octet-stream',
        'Authorization': 'Bearer ' + token
    }

    return requests.post(config.url + '/api/V1/uploadbusinessobjectattachment/filename/' + filename +
                         '/busobid/' + str(busObId) + '/publicid/' + str(publicid) +
                         '/offset/' + str(0) + '/totalsize/' + str(totalsize), data=body, headers=auth_header)
