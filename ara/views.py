from rest_framework import viewsets

from ara.models import Playbook
from ara.serializers import PlaybookSerializer, FileSerializer

from rest_framework.decorators import action
from rest_framework.response import Response


class PlaybookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows playbooks to be viewed or edited.
    """

    queryset = Playbook.objects.all()
    serializer_class = PlaybookSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "files":
            return FileSerializer

    @action(detail=True, methods=["get"])
    def files(self, request):
        # get query params
        print(
            f"request.query_params: {self.request.query_params}======================================"
        )

        playbook = self.get_object()
        files = playbook.files.all()
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("labels")
