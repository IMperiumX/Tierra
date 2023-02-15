from django.db import models
from django.contrib.auth import get_user_model

from librephotos.models import Person
from librephotos.mixins import ClusterMixin

User = get_user_model()


class Cluster(ClusterMixin, models.Model):
    mean_face_encoding = models.TextField()
    cluster_id = models.IntegerField(null=True)
    name = models.TextField(null=True)

    person = models.ForeignKey(
        Person,
        on_delete=models.SET(Person.get_unknown_person),
        related_name="clusters",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET(User.get_deleted_user),
        default=None,
        null=True,
    )

    def __str__(self):
        return f"{self.id}"
