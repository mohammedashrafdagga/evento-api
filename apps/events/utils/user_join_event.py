from rest_framework import serializers
from apps.events.models import Participant, Event
from django.contrib.auth import get_user_model


User = get_user_model()


class UserJoinEventServices:
    @staticmethod
    def check_user_already_join(event, user):
        if Participant.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError(
                detail="You have already joined this event."
            )

    @staticmethod
    def check_user_not_host_event(event, user):
        if event.host == user:
            raise serializers.ValidationError(
                detail="You cannot join an event that you are hosting."
            )

    @staticmethod
    def check_user_host_event(event, user):
        if event.host != user:
            raise serializers.ValidationError(
                detail="The User Send Request is not Host of event."
            )
