import uuid
import datetime
import copy

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ConflictError

from django.conf import settings
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework import serializers

from . import app_serializers
from . import models

from rest_framework.views import exception_handler

es = Elasticsearch(settings.ELASTICSEARCH["hosts"])

class TestViewset(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = app_serializers.TestSerializer

    def list(self, request, *args, **kwargs):
        offset = request.query_params.get("offset", 0)
        limit = request.query_params.get("limit", 10)
        try:
            res = es.search(index="test_12", doc_type="one", size=limit, from_=offset)
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res["hits"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            res = es.create(index="test_12", doc_type="one", id=uuid.uuid1(), body=serializer.data)
        except ConflictError as exc:
            raise exceptions.ParseError("Document is exists")
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        headers = self.get_success_headers(serializer.data)
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        try:
            res = es.get(index="test_12", doc_type="one", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type one of Index test_12".format(kwargs["pk"]))
        except Exception as exc:
            raise exceptions.APIException("内部错误, 错误类型：{}".format(type(exc)))
        return Response(res)

    def update(self, request, *args, **kwargs):
        try:
            res = es.get(index="test_12", doc_type="one", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type one of Index test_12".format(kwargs["pk"]))
        except Exception as exc:
            raise exceptions.APIException("内部错误, 错误类型：{}".format(type(exc)))
        his_data = res["_source"]
        partial = kwargs.get("partial", False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        data = copy.copy(his_data)
        is_equal = True
        for k,v in serializer.validated_data.items():
            if k[0] == "S":
                continue
            if isinstance(serializer.fields.fields[k], serializers.DateTimeField):
                if isinstance(v, list):
                    v = list(map(lambda x: x.isoformat(), v))
                else:
                    v = v.isoformat()
            data[k] = v
            if his_data[k] != v:
                is_equal = False
                break
        if is_equal:
            raise exceptions.ParseError(detail="No field changes")
        his_data.pop("S_creator")
        his_data.pop("S_creation_time")
        his_data["S_data_id"] = kwargs["pk"]
        his_data["S_changer"] = request.user.username
        his_data["S_update_time"] = datetime.datetime.now()
        try:
            es.index(index="test_22", doc_type="one", id=uuid.uuid1(), body=his_data)
            res = es.index(index="test_12", doc_type="one", id=kwargs["pk"], body=data)
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        try:
            res = es.get(index="test_12", doc_type="one", id=kwargs["pk"])
            data = res["_source"]
            data["S_delete_time"] = datetime.datetime.now().isoformat()
            data["S_delete_people"] = request.user.username
            res = es.create(index="test_32", doc_type="one", id=kwargs["pk"], body=data)
            es.delete(index="test_12", doc_type="one", id=kwargs["pk"])
            es.delete_by_query(index="test_22", doc_type="one", body={"query": {"match": {"S_data_id": kwargs["pk"]}}})
        except NotFoundError as exc:
            raise exceptions.ParseError("Document {} was not found in Type one of Index test_12".format(kwargs["pk"]))
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型： {}".format(type(exc)))
        return Response(res, status=status.HTTP_204_NO_CONTENT)

# t = TestViewset()
# t.paginate_queryset()

class Test2Viewset(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = app_serializers.TestSerializer
    def list(self, request, *args, **kwargs):
        # raise NotFoundError()
        a = 1/0
        print(request.body)
        print(request.data)
        return Response("list")
    def update(self, request, *args, **kwargs):
        return Response("update")

class RecordDataViewset(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            res = es.search(index="test_22", doc_type="one", body={"query": {"match": {"S_data_id": kwargs["pk"]}}})
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type one of Index test_12".format(kwargs["pk"]))
        except Exception as exc:
            raise exceptions.APIException("内部错误, 错误类型：{}".format(type(exc)))

        return Response(res["hits"])

class DeletedDataViewset(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            res = es.get(index="test_32", doc_type="one", id=kwargs["pk"])
        except NotFoundError as exc:
            raise exceptions.NotFound("Document {} was not found in Type one of Index test_12".format(kwargs["pk"]))
        except Exception as exc:
            raise exceptions.APIException("内部错误, 错误类型：{}".format(type(exc)))
        return Response(res)


class PersonViewset(viewsets.ModelViewSet):
    serializer_class = app_serializers.PersonSerializer
    queryset = models.Person.objects.all()

    def list(self, request, *args, **kwargs):
        raise Exception("custome")
