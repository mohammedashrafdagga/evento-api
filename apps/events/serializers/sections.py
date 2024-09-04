from rest_framework import serializers
from apps.events.models import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            "id",
            "name",
            "description",
            "speaker",
            "location",
            "start_datetime",
            "end_datetime",
            "event",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "event": {"write_only": True},
        }
