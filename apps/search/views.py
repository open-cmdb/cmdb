
from elasticsearch.exceptions import RequestError, NotFoundError

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import exceptions

from . import app_serializers
from utils.es import es

# Create your views here.

class SearchDataViewset(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    _doc_type = "data"
    serializer_class = app_serializers.SearchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # indices = ",".join(data["indices"])
        indices = data["indices"] if data["indices"] else "_all"
        sort = ",".join(reversed(list(map(lambda i:":".join(i), data["sort"].items()))))
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

class SearchDeletedDataViewset(SearchDataViewset):
    _doc_type = "deleted-data"
    serializer_class = app_serializers.SearchDeletedSerializer
