from rest_framework import serializers
from .models import Event, WaitingList
from django.contrib.auth import get_user_model

User = get_user_model()

# validate the event is exists
def validate_event_exists(value):
    if not Event.objects.filter(id=value).exists():
        raise serializers.ValidationError(detail="Event dose not exist")

    return value


def validate_user_exists(value):
    if not User.objects.filter(id=value).exists():
        raise serializers.ValidationError(detail="User dose not exist")
    return value


def validate_accept_user(data):
    if not WaitingList.objects.filter(
        user__id=data["user_id"], event__id=data["event_id"]
    ).exists():
        raise serializers.ValidationError(
            detail="The User is not related with event in Waiting List"
        )

    return data
