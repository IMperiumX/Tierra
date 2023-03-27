from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "librephotos"

router = routers.DefaultRouter()

router.register(r"photos", views.PhotoViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
