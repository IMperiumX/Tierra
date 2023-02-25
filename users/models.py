import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from .managers import CustomUserManager


class UserMixin:
    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_deleted_user(self):
        deleted_user = self.objects.get_or_create(username="deleted")[0]
        if deleted_user.is_active is not False:
            deleted_user.is_active = False
            deleted_user.save()
        return deleted_user


class User(UserMixin, AbstractUser):
    """
    Default custom user model for tierra.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    scan_directory = models.CharField(max_length=512, db_index=True)
    confidence = models.FloatField(default=0.1, db_index=True)
    confidence_person = models.FloatField(default=0.9)
    image_scale = models.FloatField(default=1)
    semantic_search_topk = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to="avatars", null=True)
    transcode_videos = models.BooleanField(default=False)

    favorite_min_rating = models.IntegerField(
        default=settings.DEFAULT_FAVORITE_MIN_RATING, db_index=True
    )

    SaveMetadataToDisk = models.TextChoices(
        "SaveMetadataToDisk", "OFF MEDIA_FILE SIDECAR_FILE"
    )
    save_metadata_to_disk = models.TextField(
        choices=SaveMetadataToDisk.choices, default=SaveMetadataToDisk.OFF
    )

    default_timezone = models.TextField(
        choices=[(x, x) for x in pytz.all_timezones],
        default="UTC",
    )

    objects = CustomUserManager()
