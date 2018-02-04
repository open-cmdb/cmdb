from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch.exceptions import ElasticsearchException

from elasticsearch_dsl import Search

# es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
es = Elasticsearch(hosts=["http://www.google.com:9400"])
indices_client = IndicesClient(es)
# es = Elasticsearch(hosts=["http://127.0.0.1:8000"])
# es = Elasticsearch(hosts=["http://www.google.com:9400"])
# es.cluster.health(wait_for_status='yellow', request_timeout=3)
# try:
#     res = es.search(index="test_122", doc_type="one", body={"query": {"match": {"S_data_id": "211"}}})
#     print(res)
# except Exception as exc:
#     print("timeout")
# es.cluster.health(request_timeout=3)

# res = es.delete(index="test_12", doc_type="one", id="cf97cc46-0758-11e8-91f9-70188becb8a9")

# body = {"version":True,"size":500,"sort":[{"_score":{"order":"desc"}}],"query":{"query_string":{"query":"","analyze_wildcard":True}},"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[], "from": 100}
#
# try:
#     # res = es.search(index="test_22", q="name:host-*", analyze_wildcard=True, sort="age:asc,height:desc",from_=4, size=2)
#     # res = es.search(index="test", q="user-name:'zhangsan'", analyze_wildcard=True,from_=0, size=20)
#     s = Search(using=es, index="test").query("match", user_name="zhangsan")
#     res = s.execute()
# except Exception as exc:
#     print(exc)
#     exit(1)
# print(res)
# for i in res:
#     print(i)
#
# for item in res["hits"]["hits"]:
#     print(item["_source"]["user-name"])

try:
    raise ElasticsearchException()
except Exception as exc:
    print(type(exc))

# res = es.index(index="test_22..", doc_type="data", op_type="create", body={})
try:
    res = indices_client.create(index="test-123")
except Exception as exc:
    print("exc")
    print(str(exc))
    exit(1)
else:
    print("else")
# res = indices_client.delete(index="server-logic-1")
print(res)