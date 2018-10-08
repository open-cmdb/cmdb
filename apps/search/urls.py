
from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register("data-lucene", views.DataLuceneViewSet, base_name="data-lucene")
router.register("deleted-data-lucene", views.DeletedDataLuceneViewset, base_name="deleted-data-lucene")
router.register("data-dsl", views.DataDSLViewSet, base_name="data-dsl")
router.register("deleted-data-dsl", views.DeleteDataDSLViewSet, base_name="deleted-data-dsl")


urlpatterns = [
    url(r'^', include(router.urls))
]
