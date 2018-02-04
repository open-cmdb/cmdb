import uuid
import datetime

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from django.conf import settings

from rest_framework import serializers
from rest_framework import exceptions

from . import models

es = Elasticsearch(settings.ELASTICSEARCH["hosts"])

# class TestHistorySerializer(serializers.Serializer):
#     __changer = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())
#     __update_time = serializers.DateTimeField(read_only=True, format="iso-8601", default=datetime.datetime.now)
#     name = serializers.CharField(max_length=1000, allow_blank=True)
#     age = serializers.IntegerField(allow_null=True)
#     height = serializers.FloatField()
#     hobbys = serializers.ListField(child=serializers.CharField(max_length=100))
#     last_login = serializers.DateTimeField(format="iso-8601",)


class TestSerializer(serializers.Serializer):
    S_creator = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())
    S_creation_time = serializers.DateTimeField(read_only=True, format="iso-8601", default=datetime.datetime.now)
    name = serializers.CharField(max_length=1000, allow_blank=True)
    age = serializers.IntegerField(allow_null=True)
    height = serializers.FloatField()
    hobbys = serializers.ListField(child=serializers.CharField(max_length=100))
    last_login = serializers.DateTimeField(format="iso-8601",)

    # def create(self, validated_data):
    #     try:
    #         res = es.index(index="test_12", doc_type="one", id=uuid.uuid1(), body=self.data)
    #     except Exception as exc:
    #         raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
    #     return res
    #
    # def update(self, instance, validated_data):
    #     try:
    #         res = es.get(index="test_12", doc_type="one", id=instance)
    #     except NotFoundError:
    #         raise exceptions.NotFound("Document {} was not found in type one of index test_12")
    #     his_data = res["_source"]
    #     is_equal = True
    #     print(type(self.data))
    #     for k,v in his_data.items():
    #         if k[0] == "_":
    #             continue
    #         if self.data[k] != v:
    #             is_equal = False
    #             break
    #     if is_equal:
    #         raise exceptions.ValidationError("No field changes")
    #     his_data.pop["_creator"]
    #     his_data.pop["_creation_time"]
    #     his_data["_id"] = instance
    #     his_data["_changer"] = self.user.username
    #     his_data["_update_time"] = datetime.datetime.now()
    #     try:
    #         es.index(index="test_22", doc_type="one", id=instance, body=his_data)
    #         res = es.index(index="test_12", doc_type="one", id=instance, body=self.data)
    #     except Exception as exc:
    #         raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
    #     return res


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = "__all__"