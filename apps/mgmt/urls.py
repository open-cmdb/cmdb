
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter(trailing_slash=False)
router.register("table", views.TableViewset)
router.register("user", views.UserViewset)

app_name = "mgmt"

urlpatterns = router.urls