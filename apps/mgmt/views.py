
from django.conf import settings

from elasticsearch.exceptions import NotFoundError

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status

from . import app_serializers
from . import models
from utils.es import es
from . import initialize
from utils.es import indices_client

# Create your views here.
class TableViewset(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet,):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = app_serializers.TableSerializer
    queryset = models.Table.objects.all()

    def is_data_raise(self, table_name):
        try:
            res = es.search(index=table_name)
        except NotFoundError:
            return
        except Exception as exc:
            raise exceptions.APIException("内部错误，错误类型:{}".format(type(exc)))
        if res["hits"]["total"]:
            raise exceptions.ParseError("表中已有数据，如需删除或更改表请将表清空后操作")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table = serializer.save()
        initialize.add_table(table)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.is_data_raise(instance.name)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        initialize.delete_table(instance)
        table = serializer.save()
        initialize.add_table(table)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.is_data_raise(instance.name)
        initialize.delete_table(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)