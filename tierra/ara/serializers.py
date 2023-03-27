from rest_framework import serializers

from .models import File, Playbook


class PlaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playbook
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
