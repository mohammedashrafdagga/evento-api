from rest_framework import serializers
from .models import Event
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
