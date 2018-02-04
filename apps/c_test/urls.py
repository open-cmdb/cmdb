from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from . import views

# from django.contrib.auth.decorators import login_required

router = SimpleRouter(trailing_slash=False)
router.register("data", views.TestViewset, base_name="test")
router.register("record_data", views.RecordDataViewset, base_name="record_data")
router.register("deleted_data", views.DeletedDataViewset, base_name="delete_data")
router.register("test-2", views.Test2Viewset, base_name="test-2")
router.register("person", views.PersonViewset)


urlpatterns = router.urls