from ara.models import Playbook, File

from rest_framework import serializers
import pysnooper


class PlaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playbook
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
