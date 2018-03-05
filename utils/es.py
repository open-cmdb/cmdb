from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from django.conf import settings

es = Elasticsearch(hosts=settings.ELASTICSEARCH["hosts"],
                   sniff_on_start=True,
                   # refresh nodes after a node fails to respond
                   sniff_on_connection_fail=True,
                   # and also every 60 seconds
                   sniffer_timeout=12,
                   http_auth=(settings.ELASTICSEARCH["user"], settings.ELASTICSEARCH["password"])
                   )


indices_client = IndicesClient(es)