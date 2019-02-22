import json
import random
import datetime
import requests

username = "admin"
password = "cmdbcmdb"

url_prefix = "http://cmdb.mmtweb.xyz"
# url_prefix = "http://localhost:8000"

record_count = 0


def get_token():
    response = requests.post(url_prefix+"/api/v1/token", json.dumps({"username": username, "password": password}), headers={"Content-Type": "application/json"})
    if response.status_code >= 300:
        raise Exception("Get token fail")
    print("Get token success ({})".format(response.json()["token"]))
    return response.json()["token"]


def create_table(token):
    data = {
        "name": "physical-server",
        "alias": "物理服务器",
        "readme": "记录公司所有物理服务器信息",
        "fields": [
            {
                "name": "server-name",
                "alias": "服务器名",
                "type": 0,
                "required": True,
            },
            {
                "name": "responsible",
                "alias": "负责人",
                "type": 0,
                "required": True
            },
            {
                "name": "brand",
                "alias": "品牌",
                "type": 0,
                "required": True
            },
            {
                "name": "model",
                "alias": "型号",
                "type": 0,
                "required": True
            },
            {
                "name": "purchase-time",
                "alias": "采购时间",
                "type": 3,
                "required": True
            },
            {
                "name": "price",
                "alias": "价格",
                "type": 2,
                "required": True
            },
            {
                "name": "cpu-model",
                "alias": "处理器型号",
                "type": 0,
                "required": True
            },
            {
                "name": "core-num",
                "alias": "内核个数",
                "type": 1,
                "required": True
            },
            {
                "name": "memory-size",
                "alias": "内存大小",
                "type": 0,
                "required": True
            },
            {
                "name": "network-port-num",
                "alias": "网口个数",
                "type": 1,
                "required": True
            },
            {
                "name": "hard-disk",
                "alias": "硬盘信息",
                "type": 1,
                "is_multi": True
            }
        ]
    }
    response = requests.post(url_prefix+"/api/v1/mgmt/table", json.dumps(data), headers={"Content-Type": "application/json", "Authorization": token})
    if response.status_code >= 300:
        raise Exception("创建表失败：{}".format(response.text))
    print("Create table succuessfully")


def add_record(token, table_name):

    server_name_prefix = "rd-bigdata"
    global record_count
    record_count += 1

    data = {
        "server-name": "{}-{}".format(server_name_prefix, record_count),
        "responsible": random.choice(["刘一", "陈二", "张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十"]),
        "brand": random.choice(["Huawei", "Dell", "IBM", "Inspur", "HP"]),
        "model": random.choice(["RH5885H", "E9000", "X6000", "RH1288", "RH2288", "5288 V3", "PowerEdge R730", "PowerEdge R720", "PowerEdge R430", "PowerEdge R540", "PowerEdge R910"]),
        "purchase-time": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 2000))).isoformat(),
        "price": random.randint(1300, 520000),
        "cpu-model": random.choice(["Intel Xeon E7-8870", "Intel Xeon E7-8890 v4", "Intel Xeon E7-4820", "Intel Xeon E5-2650", "Intel Xeon E5-2680 v2", "Intel Xeon E5-2670", "Intel Xeon E3-1230 v2", "Intel Xeon E3-1230 v3"]),
        "core-num": random.choice([2, 4, 8, 16, 32, 48, 96, 64]),
        "memory-size": random.choice([512, 324, 256, 128, 64, 32, 16, 8, 4, 2, 1024]),
        "hard-disk": [random.choice([128, 256, 300, 512, 320, 600, 400, 500])] * random.randint(1, 12),
        "network-port-num": random.choice([2, 4, 6, 8]),
        "used": random.randint(0, 1)
    }
    response = requests.post(url_prefix+"/api/v1"
                                        "/data/"+table_name, json.dumps(data), headers={"Content-Type": "application/json", "Authorization": token})
    if response.status_code >=300:
        print(response.text)
        raise Exception("Add record fail")
    print("{}-{} add successfully".format(url_prefix, record_count))


if __name__ == '__main__':
    token = get_token()
    token = "JWT " + token
    print(token)
    # create_table(token)
    for i in range(1000):
        add_record(token, "physical-server")
