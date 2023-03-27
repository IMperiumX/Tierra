from librephotos.models import Photo
from librephotos.serializers import PhotoSerializer
from rest_framework import mixins, viewsets


class PhotoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
