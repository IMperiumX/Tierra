# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import sites
from librephotos.models import Cluster, Face, Person, Photo


class MyAdminSite(sites.AdminSite):
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        # serialize the app list to a list of dicts
        from pprint import pprint

        print(app_dict)
        app_list = [
            app_dict[app]
            for app in app_dict
            if app in ["librephotos", "auth", "contenttypes"]
        ]
        app_list.sort(key=lambda x: x["name"])
        return app_list


mysite = MyAdminSite()
admin.site = mysite
sites.site = mysite


@admin.register(Photo, Person, Cluster, Face)
class PhotoAdmin(admin.ModelAdmin):
    ...
    # list_display = (
    #     "image_paths",
    #     "image_hash",
    #     "thumbnail_big",
    #     "square_thumbnail",
    #     "square_thumbnail_small",
    #     "aspect_ratio",
    #     "added_on",
    #     "exif_gps_lat",
    #     "exif_gps_lon",
    #     "exif_timestamp",
    #     "exif_json",
    #     "geolocation_json",
    #     "captions_json",
    #     "dominant_color",
    #     "search_captions",
    #     "search_location",
    #     "timestamp",
    #     "rating",
    #     "deleted",
    #     "hidden",
    #     "video",
    #     "video_length",
    #     "size",
    #     "fstop",
    #     "focal_length",
    #     "iso",
    #     "shutter_speed",
    #     "camera",
    #     "lens",
    #     "width",
    #     "height",
    #     "focalLength35Equivalent",
    #     "subjectDistance",
    #     "digitalZoomRatio",
    #     "owner",
    #     "public",
    #     "clip_embeddings",
    #     "clip_embeddings_magnitude",
    # )
    # list_filter = (
    #     "added_on",
    #     "exif_timestamp",
    #     "timestamp",
    #     "deleted",
    #     "hidden",
    #     "video",
    #     "owner",
    #     "public",
    # )
    # raw_id_fields = ("shared_to",)


# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "kind", "cover_photo", "cluster_owner")
#     list_filter = ("cover_photo", "cluster_owner")
#     search_fields = ("name",)


# @admin.register(Cluster)
# class ClusterAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "mean_face_encoding",
#         "cluster_id",
#         "name",
#         "person",
#         "owner",
#     )
#     list_filter = ("person", "owner")
#     search_fields = ("name",)


# @admin.register(Face)
# class FaceAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "image",
#         "image_path",
#         "person_label_is_inferred",
#         "person_label_probability",
#         "location_top",
#         "location_bottom",
#         "location_left",
#         "location_right",
#         "encoding",
#         "photo",
#         "person",
#         "cluster",
#     )
#     list_filter = ("person_label_is_inferred", "photo", "person", "cluster")
