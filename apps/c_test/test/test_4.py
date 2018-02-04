from elasticsearch import Elasticsearch

es = Elasticsearch()
try:
    res = es.get(index="test_12", doc_type="one", id="5eaaf154-0684-11e8-91f9-70188becb8a")
except Exception as exc:
    print(type(exc))
# print(res)
