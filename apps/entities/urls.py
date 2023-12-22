from rest_framework import routers
from apps.entities import views

app_name = "apps.entities"

router = routers.SimpleRouter()
router.register(r"entities", views.EntityViewSet)

urlpatterns = router.urls
