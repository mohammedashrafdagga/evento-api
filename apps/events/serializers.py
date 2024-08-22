from .models import Event, Section
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "profile_image")


# Section Serializer
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

    # validate
    def validate(self, data):
        if self.context["request"].method == "POST":
            event = data.get("event")
            user = self.context["request"].user

            if not event.host == user:
                raise serializers.ValidationError(
                    "You can only add sections to events that you host."
                )
        return data

    def update(self, instance, validated_data):
        # validate event in update status
        if self.context["request"].method == "PUT":
            event = validated_data["event"]
            if event != instance.event:
                raise serializers.ValidationError(
                    "The event enter not same for default event."
                )
        return super().update(instance, validated_data)


class EventSerializer(serializers.ModelSerializer):
    participants = UserEventSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "location",
            "start_date",
            "background_image",
            "end_date",
            "host",
            "participants",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "host": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        if user.user_type != "hosting":
            raise serializers.ValidationError(
                "You do not have permission to create events."
            )
        return attrs

    def create(self, validated_data):
        host = self.context["request"].user
        event = Event.objects.create(host=host, **validated_data)
        return event


# Event Serializer
class EventSectionSerializer(EventSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    participants = UserEventSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "location",
            "start_date",
            "background_image",
            "end_date",
            "host",
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
