import requests
import config
import json

def main():
    data = {}
    requests.get(config.url, )
    response = requests.post(config.url + "/api/V1/getbusinessobjecttemplate")
    print(response)


main()