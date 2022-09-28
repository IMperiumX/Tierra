from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="URI - Backend API",
        default_version="v1",
        description="Underlying api for URI website",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("signup/", TemplateView.as_view(template_name="signup.html"), name="signup"),
    path(
        "email-verification/",
        TemplateView.as_view(template_name="email_verification.html"),
        name="email-verification",
    ),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("logout/", TemplateView.as_view(template_name="logout.html"), name="logout"),
    path(
        "password-reset/",
        TemplateView.as_view(template_name="password_reset.html"),
        name="password-reset",
    ),
    path(
        "password-reset/confirm/",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password-reset-confirm",
    ),
    path(
        "user-details/",
        TemplateView.as_view(template_name="user_details.html"),
        name="user-details",
    ),
    path(
        "password-change/",
        TemplateView.as_view(template_name="password_change.html"),
        name="password-change",
    ),
    path(
        "resend-email-verification/",
        TemplateView.as_view(template_name="resend_email_verification.html"),
        name="resend-email-verification",
    ),
    # url generate email content
    re_path(
        "password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    # user management urls
    path("api/v1/", include("dj_rest_auth.urls")),
    path("api/v1/registration/", include("dj_rest_auth.registration.urls")),
    path("account/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path(
        "accounts/profile/",
        RedirectView.as_view(url="/", permanent=True),
        name="profile-redirect",
    ),
    # Courses API
    path("api/v1/", include("courses.api.urls", namespace="courses_api")),
    # swagger urls
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
