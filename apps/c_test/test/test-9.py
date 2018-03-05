from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch()

# res = es.search(index="ddd.", doc_type="record-data", body={"query": {"constant_score": {"filter": {"term": {"S-data-id": "c4409e4a-1af4-11e8-b9d7-70188becb8"}}}}})
res = es.search( body={"query": {"term": {"sss": "ccc"}}})

# s = Search(using=es, index="dfds", doc_type="data").filter("term", sdda="abc\-def")
# response = s.execute()
print(res["hits"]["hits"])
# print(response)