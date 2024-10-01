from apps.events.models import Event, Participant
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .sections import SectionSerializer

User = get_user_model()


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "profile_image")


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserEventSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ["user"]


event_fields = [
    "id",
    "name",
    "description",
    "location",
    "start_date",
    "background_image",
    "end_date",
    "host",
]


class EventSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = event_fields + [
            "participants",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "host": {"read_only": True},
        }

    def create(self, validated_data):
        host = self.context["request"].user
        event = Event.objects.create(host=host, **validated_data)
        return event


# Event Serializer
class EventSectionSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = event_fields + [
            "participants",
            "create_at",
            "update_at",
            "sections",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "host": {"read_only": True},
            "participants": {"read_only": True},
            "create_at": {"read_only": True},
            "update_at": {"read_only": True},
        }
