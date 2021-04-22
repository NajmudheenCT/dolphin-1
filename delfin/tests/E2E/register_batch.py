from time import sleep

import requests

# Number of storage to be registered
TOTAL_STORAGES = 100

# Total wait time in seconds for all storage sync to complete
SYNC_WAIT_PERIOD_SECONDS = 300
for i in range(TOTAL_STORAGES):
    url = "http://localhost:8190/v1/storages"

    payload = "{\t\r\n\t\"model\":\"fake_driver\",\r\n    \r\n\t\"vendor\":\"fake_storage\",\r\n    \"rest\":\r\n    {" \
              "\"username\":\"test12344566111111\",\r\n\t\"password\":\"abcd\",\r\n\t\"port\": 12346," \
              "\r\n    \"host\":\"127.0.0.2\"}\r\n\t\r\n} "
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    status_code = response.status_code
    if status_code != 201:
        print("registration failed:")
        exit()
    json = response.json()
    print(" storage registered id=", json['id'])
    sleep(5)

sleep(SYNC_WAIT_PERIOD_SECONDS)
url = "http://localhost:8190/v1/storages"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
json = response.json()

for storage in json['storages']:
    # print(storage['sync_status'])
    if storage['sync_status'] != 'SYNCED':
        print('Failed sync status check for storage storage: ', storage['id'])
        exit()
print('SUCCESS')
