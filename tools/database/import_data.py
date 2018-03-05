import requests
import json
import time

data = []

is_odd = False

url_prefix = "http://cmdb.mingmingt.xyz"

def get_token():
    response = requests.post(url_prefix+"/api/v1/token", json.dumps({"username": "admin", "password": "wonders,1"}), headers={"Content-Type": "application/json"})
    if response.status_code >= 300:
        raise Exception("Get token fail: {}".format(response.text))
    print("Get token success ({})".format(response.json()["token"]))
    return response.json()["token"]

def create_table(token):
    data = {
        "name": "bank-account",
        "fields": [
            {
                "name": "account-number",
                "type": 1,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "balance",
                "type": 1,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "firstname",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "lastname",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "age",
                "type": 1,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "gender",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "address",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "employer",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "email",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "city",
                "type": 0,
                "is_multi": False,
                "requried": True
            },
            {
                "name": "state",
                "type": 0,
                "is_multi": False,
                "requried": True
            }
        ]
    }
    response = requests.post(url_prefix+"/api/v1/mgmt/table", json.dumps(data), headers={"Content-Type": "application/json", "Authorization": token})
    if response.status_code >= 300:
        raise Exception("创建表失败：{}".format(response.text))
    print("Create table succuessfully")


if __name__ == '__main__':
    token = get_token()
    token = "JWT " + token
    # create_table(token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    with open("a") as f:
        for line in f.readlines():
            is_odd = not is_odd
            if(is_odd):
                continue
            data = json.loads(line)
            data["account-number"] = data.pop("account_number")
            # time.sleep(1)
            res = requests.post(url_prefix + "/api/v1/data/bank-account", data=json.dumps(data), headers=headers)
            print(res.text)

    # if(is_odd):
    #     is_odd = not is_odd
    # data.append(line)
    # is_odd = not is_odd
#
# print(data)
# j_data = json.loads(data)
# print(j_data)