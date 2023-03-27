from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from librephotos.managers import VisiblePhotoManager
from librephotos.mixins import PhotoMixin

User = get_user_model()


class Photo(PhotoMixin, models.Model):
    image_paths = models.JSONField(default=list)
    image_hash = models.CharField(primary_key=True, max_length=64, null=False)

    thumbnail_big = models.ImageField(upload_to="thumbnails_big")

    square_thumbnail = models.ImageField(upload_to="square_thumbnails")
    square_thumbnail_small = models.ImageField(upload_to="square_thumbnails_small")

    aspect_ratio = models.FloatField(blank=True, null=True)

    added_on = models.DateTimeField(null=False, blank=False, db_index=True)

    exif_gps_lat = models.FloatField(blank=True, null=True)
    exif_gps_lon = models.FloatField(blank=True, null=True)
    exif_timestamp = models.DateTimeField(blank=True, null=True, db_index=True)

    exif_json = models.JSONField(blank=True, null=True)

    geolocation_json = models.JSONField(blank=True, null=True, db_index=True)
    captions_json = models.JSONField(blank=True, null=True, db_index=True)

    dominant_color = models.TextField(blank=True, null=True)

    search_captions = models.TextField(blank=True, null=True, db_index=True)
    search_location = models.TextField(blank=True, null=True, db_index=True)

    timestamp = models.DateTimeField(blank=True, null=True, db_index=True)
    rating = models.IntegerField(default=0, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    hidden = models.BooleanField(default=False, db_index=True)
    video = models.BooleanField(default=False)
    video_length = models.TextField(blank=True, null=True)
    size = models.IntegerField(default=0)
    fstop = models.FloatField(blank=True, null=True)
    focal_length = models.FloatField(blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)
    shutter_speed = models.TextField(blank=True, null=True)
    camera = models.TextField(blank=True, null=True)
    lens = models.TextField(blank=True, null=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    focalLength35Equivalent = models.IntegerField(blank=True, null=True)
    subjectDistance = models.FloatField(blank=True, null=True)
    digitalZoomRatio = models.FloatField(blank=True, null=True)

    owner = models.ForeignKey(
        User, on_delete=models.SET(User.get_deleted_user), default=None
    )

    shared_to = models.ManyToManyField(User, related_name="photo_shared_to")

    public = models.BooleanField(default=False, db_index=True)
    clip_embeddings = ArrayField(
        models.FloatField(blank=True, null=True), size=512, null=True
    )
    clip_embeddings_magnitude = models.FloatField(blank=True, null=True)

    objects = models.Manager()
    visible = VisiblePhotoManager()

    class Meta:
        app_label = "librephotos"

    def __str__(self):
        return f"{self.image_hash}"
