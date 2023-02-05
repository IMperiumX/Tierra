from django.db import models
from django.db.models import Q


class VisiblePhotoQueryset:
    def filter_for_visible_photos(self):
        return self.filter(
            Q(hidden=False) & Q(aspect_ratio__isnull=False) & Q(deleted=False)
        )


class VisiblePhotoManager(models.Manager.from_queryset(VisiblePhotoQueryset)):
    pass
