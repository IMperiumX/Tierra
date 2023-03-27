from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from librephotos.conf import KIND_CLUSTER, KIND_UNKNOWN, KIND_USER
from librephotos.mixins import PersonMixin
from librephotos.models import Photo

User = get_user_model()


class Person(PersonMixin, models.Model):
    KIND_CHOICES = (
        (KIND_USER, _("User Labelled")),
        (KIND_CLUSTER, _("Cluster ID")),
        (KIND_UNKNOWN, _("Unknown Person")),
    )

    name = models.CharField(blank=False, max_length=128)
    kind = models.CharField(choices=KIND_CHOICES, max_length=10)

    cover_photo = models.ForeignKey(
        Photo,
        related_name="person",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    cluster_owner = models.ForeignKey(
        User,
        related_name="owner",
        on_delete=models.SET(User.get_deleted_user),
        default=None,
        null=True,
    )

    class Meta:
        app_label = "librephotos"

    def __str__(self):
        return f"{self.id}"
