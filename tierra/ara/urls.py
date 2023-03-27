from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "ara"

router = routers.DefaultRouter()

router.register(
    r"playbooks",
    views.PlaybookViewSet,
)

urlpatterns = [
    path("", include(router.urls)),
]
