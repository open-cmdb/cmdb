
from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register("data", views.SearchDataViewset, base_name="data")
router.register("deleted-data", views.SearchDeletedDataViewset, base_name="deleted-data")

urlpatterns = [
    url(r'^', include(router.urls))
]