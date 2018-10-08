
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter(trailing_slash=False)
router.register("table", views.TableViewset)
router.register("user", views.UserViewset)
router.register("department", views.DepartmentViewSet)

app_name = "mgmt"

urlpatterns = router.urls
