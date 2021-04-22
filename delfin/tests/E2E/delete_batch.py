from time import sleep

import requests

url = "http://localhost:8190/v1/storages"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
json = response.json()

for storage in json['storages']:
    print(storage['id'], " deleted")
    url = "http://localhost:8190/v1/storages/" + storage['id']
    response = requests.request("DELETE", url, headers=headers, data=payload)

    # print(response.text)
    sleep(1)


# print(response.text)
