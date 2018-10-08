
import re

from elasticsearch.exceptions import RequestError, NotFoundError

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import exceptions

from . import app_serializers
from mgmt import models as mgmt_models
from utils.es import es


class DataLuceneViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    _doc_type = "data"
    serializer_class = app_serializers.DataLuceneSerializer

    def get_indices(self, input_indices):
        tables = mgmt_models.Table.objects.all()
        all_indices = [table.name for table in tables]
        not_exit_indices = list(set(input_indices) - set(all_indices))
        if not_exit_indices:
            raise exceptions.ParseError(f"{not_exit_indices}不存在")
        all_perm_name = self.request.user.get_all_permission_names()
        if "read_all" in all_perm_name or self.request.user.is_staff:
            if not input_indices:
                return all_indices
            return input_indices
        has_perm_indices = [perm_name.split(".read")[0] for perm_name in all_perm_name if re.match(
                                            "^[a-z][a-z-0-9]*\.read", perm_name)]
        if not input_indices:
            if not has_perm_indices:
                raise exceptions.ParseError("您没有任何表读取权限 请联系管理员分配权限")
            return has_perm_indices
        no_perm_index = list(set(input_indices) - set(has_perm_indices))
        if no_perm_index:
            raise exceptions.PermissionDenied(f"你没有{no_perm_index}表权限")
        return input_indices

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # indices = data["indices"] if data["indices"] else "_all"
        indices = self.get_indices(data["indices"])
        sort = ",".join(reversed(list(map(lambda i: ":".join(i), data["sort"].items()))))
        try:
            res = es.search(index=indices,
                            doc_type=self._doc_type,
                            from_=data["page_size"] * (data["page"]-1),
                            size=data["page_size"],
                            sort=sort,
                            q=data["query"],
                            analyze_wildcard=True)
        except NotFoundError as exc:
            return Response({
                "hits": [],
                "max_score": None,
                "total": 0
            })
        except RequestError as exc:
            raise exceptions.ParseError("Search statement error: "+str(exc))
        return Response(res["hits"])


class DeletedDataLuceneViewset(DataLuceneViewSet):
    _doc_type = "deleted-data"
    serializer_class = app_serializers.DataLuceneSerializer

    def get_indices(self, input_indices):
        return [index + ".." for index in super().get_indices(input_indices)]


class DataDSLViewSet(DataLuceneViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # indices = data["indices"] if data["indices"] else "_all"
        indices = self.get_indices(data["indices"])
        sort = ",".join(reversed(list(map(lambda i: ":".join(i), data["sort"].items()))))
        try:
            res = es.search(index=indices,
                            doc_type=self._doc_type,
                            from_=data["page_size"] * (data["page"]-1),
                            size=data["page_size"],
                            sort=sort,
                            body=data["body"],
                            analyze_wildcard=True)
        except NotFoundError as exc:
            return Response({
                "hits": [],
                "max_score": None,
                "total": 0
            })
        except RequestError as exc:
            raise exceptions.ParseError("Search statement error: "+str(exc))
        return Response(res["hits"])


class DeleteDataDSLViewSet(DataDSLViewSet):

    def get_indices(self, input_indices):
        return [index + ".." for index in super().get_indices(input_indices)]

