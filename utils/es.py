from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from django.conf import settings

from mgmt import models as mgmt_models


es = Elasticsearch(hosts=settings.ELASTICSEARCH["hosts"],
                   # sniff_on_start=True,
                   # # refresh nodes after a node fails to respond
                   # sniff_on_connection_fail=True,
                   # # and also every 60 seconds
                   # sniffer_timeout=12,
                   http_auth=(settings.ELASTICSEARCH["username"], settings.ELASTICSEARCH["password"])
                   )


indices_client = IndicesClient(es)


class Mapping:
    MAP = {
        0: {"type": "keyword"},
        1: {"type": "long"},
        2: {"type": "double"},
        3: {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
        4: {"type": "date", "format": "yyyy-MM-dd"},
        5: {"type": "boolean"},
        6: {"type": "ip"}
    }

    def _generate_mapping(self, table):
        mapping = {}
        for field in table.fields.all():
            mapping[field.name] = self.MAP[field.type]
        return mapping

    def generate_data_mapping(self, table):
        system_mapping = {
            "S-creator": self.MAP[0],
            "S-creation-time": self.MAP[3],
            "S-last-modified": self.MAP[0]
        }
        field_mapping = self._generate_mapping(table)
        return dict(**system_mapping, **field_mapping)

    def generate_record_data_mapping(self, table):
        system_mapping = {
            "S-data-id": self.MAP[0],
            "S-changer": self.MAP[0],
            "S-update-time": self.MAP[3]
        }
        field_mapping = self._generate_mapping(table)
        return dict(**system_mapping, **field_mapping)

    def generate_deleted_data_mapping(self, table):
        system_mapping = {
            "S-delete-people": self.MAP[0],
            "S-delete-time": self.MAP[3]
        }
        field_mapping = self._generate_mapping(table)
        return dict(**system_mapping, **field_mapping)
