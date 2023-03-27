import datetime

import pytz
from django.db.models import Prefetch

utc = pytz.UTC


class PersonMixin:
    def get_photos(self, owner):
        from librephotos.models import Photo

        faces = list(
            self.faces.prefetch_related(
                Prefetch(
                    "photo",
                    queryset=Photo.objects.exclude(image_hash=None)
                    .filter(hidden=False, owner=owner)
                    .order_by("-exif_timestamp")
                    .only(
                        "image_hash",
                        "exif_timestamp",
                        "rating",
                        "owner__id",
                        "public",
                        "hidden",
                    )
                    .prefetch_related("owner"),
                )
            )
        )

        photos = [face.photo for face in faces if hasattr(face.photo, "owner")]
        photos.sort(
            key=lambda x: x.exif_timestamp or utc.localize(datetime.datetime.min),
            reverse=True,
        )
        return photos

    def get_unknown_person(owner=None):
        from librephotos.models import Person

        unknown_person: Person = Person.objects.get_or_create(
            name=Person.UNKNOWN_PERSON_NAME, cluster_owner=owner
        )[0]
        if unknown_person.kind != Person.KIND_UNKNOWN:
            unknown_person.kind = Person.KIND_UNKNOWN
            unknown_person.save()
        return unknown_person

    def get_or_create_person(name, owner=None):
        from librephotos.models import Person

        return Person.objects.get_or_create(name=name, cluster_owner=owner)[0]
