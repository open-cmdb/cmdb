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
from rest_framework.fields import empty

from utils import c_permissions
from utils.es import es
from mgmt.models import Table
from mgmt.models import Field
from . import app_serializers
from . import views

FIELD_TYPE_MAP = Field.FIELD_TYPE_MAP


def empty_none(self, val):
    if(val == ""):
        return None
    return val

# def remove_empty_str(data):
#     for k, v in data.items():
#         if v == "":
#             data.pop(k)
# def serializer_init(self, instance=None, data=empty, **kwargs):
#     if data is not empty:
#         for k,v in data.items():
#             if(v==""):
#                 data.pop(k)
#     super(Serializer, self).__init__(instance, data, **kwargs)


def add_serializer(table):
    fields = table.fields.all()
    attributes = {}
    for field in fields:
        args = {
            "label": field.alias
        }
        if not field.required:
            args["default"] = None
            args["allow_null"] = True
        if field.type == 3:
            args["format"] = "%Y-%m-%dT%H:%M:%S"
        elif field.type == 6:
            args["protocol"] = "IPv4"
        f = FIELD_TYPE_MAP[field.type](**args)
        if(field.is_multi):
            attributes[field.name] = serializers.ListField(default=[], child=f)
        else:
            attributes[field.name] = f
        # if(field.type == 0):
        #     attributes["validate_{}".format(field.name)] = empty_none
    #创建者拿到视图aQ!
    # attributes["S-creator"] = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())
    attributes["S-creation-time"] = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%S",
                                                              default=datetime.datetime.now)
    attributes["S-last-modified"] = serializers.CharField(default=None, allow_null=True, read_only=True, label="最后修改人")
    serializer = type(table.name, (Serializer, ), attributes)
    setattr(app_serializers, table.name, serializer)


def add_viewset(table):
    data_index = table.name
    record_data_index = "{}.".format(table.name)
    deleted_data_index = "{}..".format(table.name)

    def list(self, request, *args, **kwargs):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        res = es.search(index=data_index, doc_type="data", size=page_size, from_=(page-1)*page_size)
        return Response(res["hits"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data["S-creator"] = request.user.username
        try:
            res = es.create(index=data_index, doc_type="data", id=str(uuid.uuid1()).replace("-", ""), body=data)
        except ConflictError as exc:
            raise exceptions.ParseError("Document is exists")
        headers = self.get_success_headers(serializer.data)
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        try:
            res = es.get(index=data_index, doc_type="data", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", data_index))
        return Response(res)

    def update(self, request, *args, **kwargs):
        try:
            res = es.get(index=data_index, doc_type="data", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", data_index))
        partial = kwargs.get("partial", False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        his_data = res["_source"]
        data = copy.copy(his_data)
        is_equal = True
        for k, v in serializer.validated_data.items():
            if k[0] == "S":
                continue
            if isinstance(serializer.fields.fields[k], serializers.DateTimeField):
                if isinstance(v, type([])):
                    v = list(map(lambda x: x.isoformat(), v))
                elif v != None:
                    v = v.isoformat()
            data[k] = v
            if his_data[k] != v:
                is_equal = False
        if is_equal:
            raise exceptions.ParseError(detail="No field changes")
        his_data.pop("S-creator")
        his_data.pop("S-creation-time")
        his_data["S-data-id"] = kwargs["pk"]
        his_data["S-changer"] = data["S-last-modified"]
        his_data["S-update-time"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        data["S-last-modified"] = request.user.username
        his_data.pop("S-last-modified")
        es.index(index=record_data_index, doc_type="record-data", id=str(uuid.uuid1()).replace("-", ""), body=his_data)
        res = es.index(index=data_index, doc_type="data", id=kwargs["pk"], body=data)
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        try:
            res = es.get(index=data_index, doc_type="data", id=kwargs["pk"])
            data = res["_source"]
            data.pop("S-last-modified")
            data["S-delete-time"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            data["S-delete-people"] = request.user.username
            res = es.create(index=deleted_data_index, doc_type="deleted-data", id=kwargs["pk"], body=data)
            es.delete(index=data_index, doc_type="data", id=kwargs["pk"])
            es.delete_by_query(index=record_data_index, doc_type="record-data", body={"query": {"term": {"S-data-id": kwargs["pk"]}}})
        except NotFoundError as exc:
            raise exceptions.ParseError("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", table.name))
        return Response(res, status=status.HTTP_204_NO_CONTENT)

    serializer_class = getattr(app_serializers, table.name)
    viewset = type(table.name, (mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet),
                   dict(serializer_class=serializer_class, permission_classes=(c_permissions.TableLevelPermission, ),
                        list=list, create=create, retrieve=retrieve, update=update, destroy=destroy))
    setattr(views, table.name, viewset)
    return viewset
