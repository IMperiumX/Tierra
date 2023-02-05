from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Tierra - Backend API",
        default_version="v1",
        description="Underlying api for Tierra E-Learning Platform",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="yusufadell.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # user management urls
    path("api/v1/", include("dj_rest_auth.urls")),
    path("api/v1/registration/", include("dj_rest_auth.registration.urls")),
    path("account/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    # Apps API
    path(
        "api/v1/",
        include("courses.api.urls", namespace="courses-api"),
    ),
    path("api/v1/", include("ara.urls", namespace="ara-api")),
    # swagger urls
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api-docs"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # silk urls
    path("silk/", include("silk.urls", namespace="silk")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]

import dj_rest_auth
