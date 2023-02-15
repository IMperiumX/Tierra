from django.db import models
from django.db.models import Q, Case, When, Value, F, Count

from django.contrib.auth.models import UserManager


class UserQuerySet(models.QuerySet):
    def admin_users_count(self):
        return self.annotate(
            admin_users_count=Count(
                Case(
                    When(Q(is_superuser=True), then=True),
                    default=None,
                )
            )
        )

    def admin_users(self):
        return self.filter(Q(is_superuser=True))


class CustomUserManager(models.Manager.from_queryset(UserQuerySet), UserManager):
    pass
