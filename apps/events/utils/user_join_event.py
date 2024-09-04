from rest_framework import serializers
from apps.events.models import Participant, WaitingList, Event
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

    @staticmethod
    def add_user_to_event(event, user):
        # Now Adding Check if event is for all or specific
        if event.availability == "all":
            Participant.objects.create(user=user, event=event)
            message = "you are joining successfully into event"
            # send notification for User
        else:
            WaitingList.objects.create(user=user, event=event)
            message = "you are adding into Waiting List for event"

        return message

    @staticmethod
    def accept_user(user_id, event_id):
        event = Event.objects.get(id=event_id)
        user = User.objects.get(id=user_id)
        WaitingList.objects.filter(user=user, event=event).delete()
        Participant.objects.create(user=user, event=event)
