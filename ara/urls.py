from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ara import views


app_name = "ara"

router = DefaultRouter()
router.register(r"playbooks", views.PlaybookViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
