import json

from autoticket import config
import requests


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
        'busObId': '6dd53665c0c24cab86870a21cf6434ae',
        'includeAll': 'true',
        'includeRequired': 'true'
    }

    return requests.post(config.url + 'api/V1/getbusinessobjecttemplate', data=payload, headers=auth_header).json()


def createticket(fields):
    token = gettoken()

    payload = {
        "busObId": "6dd53665c0c24cab86870a21cf6434ae",
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

    return requests.post(config.url + 'api/V1/savebusinessobject', data=json.dumps(payload), headers=auth_header).json()

# TODO implement
def deleteticket(publicid):
    pass


def addattachment(body, filename, publicid, totalsize):
    token = gettoken()
    busobid = "6dd53665c0c24cab86870a21cf6434ae"

    auth_header = {
        'Accept': 'application/json',
        'Content-Type': 'application/octet-stream',
        'Authorization': 'Bearer ' + token
    }

    return requests.post(config.url + '/api/V1/uploadbusinessobjectattachment/filename/' + filename +
                         '/busobid/' + str(busobid) + '/publicid/' + str(publicid) +
                         '/offset/' + str(0) + '/totalsize/' + str(totalsize), data=body, headers=auth_header)
