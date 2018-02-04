import copy
import json
import uuid
import datetime

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ConflictError

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets

from mgmt.models import Table
from . import app_serializers
from . import views
from utils.es import es
from mgmt.models import Field

FIELD_TYPE_MAP = Field.FIELD_TYPE_MAP

def add_serializer(table):
    fields = table.fields.all()
    attributes = {}
    for field in fields:
        if(field.type == 3):
            f = FIELD_TYPE_MAP[field.type](format="iso-8601", allow_null=not field.requried)
        else:
            f = FIELD_TYPE_MAP[field.type](allow_null=not field.requried)
        if(field.is_multi):
            attributes[field.name] = serializers.ListField(child=f)
        else:
            attributes[field.name] = f
    attributes["S-creator"] = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())
    attributes["S-creation-time"] = serializers.DateTimeField(read_only=True, format="iso-8601", default=datetime.datetime.now)
    serializer = type(table.name, (Serializer, ), attributes)
    setattr(app_serializers, table.name, serializer)


def add_viewset(table):
    data_index = table.name
    record_data_index = "{}.".format(table.name)
    deleted_data_index = "{}..".format(table.name)

    def list(self, request, *args, **kwargs):
        offset = request.query_params.get("offset", 0)
        limit = request.query_params.get("limit", 10)
        try:
            res = es.search(index=data_index, doc_type="data", size=limit, from_=offset)
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res["hits"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            res = es.create(index=data_index, doc_type="data", id=uuid.uuid1(), body=serializer.data)
        except ConflictError as exc:
            raise exceptions.ParseError("Document is exists")
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        headers = self.get_success_headers(serializer.data)
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        try:
            res = es.get(index=data_index, doc_type="data", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", data_index))
        except Exception as exc:
            raise exceptions.APIException("内部错误, 错误类型：{}".format(type(exc)))
        return Response(res)

    def update(self, request, *args, **kwargs):
        try:
            res = es.get(index=data_index, doc_type="data", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", data_index))
        except Exception as exc:
            raise exceptions.APIException("内部错误, 错误类型：{}".format(type(exc)))
        partial = kwargs.get("partial", False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        his_data = res["_source"]
        data = copy.copy(his_data)
        is_equal = True
        for k,v in serializer.validated_data.items():
            if k[0] == "S":
                continue
            if isinstance(serializer.fields.fields[k], serializers.DateTimeField):
                if isinstance(v, type([])):
                    v = list(map(lambda x: x.isoformat(), v))
                else:
                    v = v.isoformat()
            data[k] = v
            if his_data[k] != v:
                is_equal = False
                break
        if is_equal:
            raise exceptions.ParseError(detail="No field changes")
        his_data.pop("S-creator")
        his_data.pop("S-creation-time")
        his_data["S-data-id"] = kwargs["pk"]
        his_data["S-changer"] = request.user.username
        his_data["S-update-time"] = datetime.datetime.now()
        try:
            es.index(index=record_data_index, doc_type="data", id=uuid.uuid1(), body=his_data)
            res = es.index(index=data_index, doc_type="data", id=kwargs["pk"], body=data)
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        try:
            res = es.get(index=data_index, doc_type="data", id=kwargs["pk"])
            data = res["_source"]
            data["S-update-time"] = datetime.datetime.now().isoformat()
            data["S-delete-people"] = request.user.username
            res = es.create(index=deleted_data_index, doc_type="data", id=kwargs["pk"], body=data)
            es.delete(index=data_index, doc_type="data", id=kwargs["pk"])
            es.delete_by_query(index=record_data_index, doc_type="data", body={"query": {"match": {"S-data-id": kwargs["pk"]}}})
        except NotFoundError as exc:
            raise exceptions.ParseError("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", table.name))
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res, status=status.HTTP_204_NO_CONTENT)

    serializer_class = getattr(app_serializers, table.name)
    viewset = type(table.name, (mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet), dict(serializer_class=serializer_class, list=list, create=create, retrieve=retrieve, update=update, destroy=destroy))
    setattr(views, table.name, viewset)
    return viewset