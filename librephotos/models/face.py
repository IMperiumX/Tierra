from django.db import models

from librephotos.mixins import FaceMixin

from . import Cluster, Person, Photo


class Face(FaceMixin, models.Model):
    image = models.ImageField(upload_to="faces", null=True)
    image_path = models.FilePathField(
        path="/home/yusufadell/Pictures/Wallpapers",
        match="foo.*",
        recursive=True,
    )

    person_label_is_inferred = models.BooleanField(null=True)
    person_label_probability = models.FloatField(default=0.0)

    location_top = models.IntegerField()
    location_bottom = models.IntegerField()
    location_left = models.IntegerField()
    location_right = models.IntegerField()

    encoding = models.TextField()

    photo = models.ForeignKey(
        Photo,
        related_name="faces",
        on_delete=models.CASCADE,
        blank=False,
        null=True,
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.DO_NOTHING,
        related_name="faces",
    )
    cluster = models.ForeignKey(
        Cluster,
        related_name="faces",
        on_delete=models.SET(Cluster.get_unknown_cluster),
        blank=True,
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "person_label_is_inferred",
                    "person_label_probability",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.id}"
