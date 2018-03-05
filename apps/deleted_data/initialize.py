from elasticsearch.exceptions import NotFoundError

from django.conf import settings

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets

from . import views
from utils.es import es

def add_viewset(table):
    data_index = table.name
    record_data_index = "{}.".format(table.name)
    deleted_data_index = "{}..".format(table.name)

    def list(self, request, *args, **kwargs):
        offset = request.query_params.get("offset", 0)
        limit = request.query_params.get("limit", 10)
        try:
            res = es.search(index=deleted_data_index, doc_type="deleted-data", size=limit, from_=offset)
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res["hits"])

    def retrieve(self, request, *args, **kwargs):
        try:
            res = es.get(index=deleted_data_index, doc_type="data", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type {} of Index {}".format(kwargs["pk"],"data", table.name))
    viewset = type(table.name, (mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet), dict(list=list, retrieve=retrieve))
    setattr(views, table.name, viewset)
    return viewset