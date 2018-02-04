
import json

import requests

from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IiIsImV4cCI6MTUxNzU4ODQ4OCwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJsaXNpIn0.OEpoYSuprzlFREuv7W7BHBIKsTakZy2eZr-rtowAfMU"
}

data = {
	"indices": ["test_22", "test_12"],
    "size": 20,
	"sort": {
			"age": "desc",
			"last_login": "desc"
		}
}

res = requests.post("http://127.0.0.1:8000/api/v1/search/data", headers=headers, data=json.dumps(data))

res_data = res.json()
print(res_data)
for i in res_data["hits"]:
    print(i["_source"]["age"], i["_source"]["last_login"])