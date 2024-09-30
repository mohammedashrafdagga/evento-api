# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section, Participant, WaitingList
from apps.notification.models import Notification



@receiver(post_save, sender=Section)
def send_notification_to_participant(sender, instance, created, **kwargs):
    event = instance.event
    participants = Participant.objects.filter(event=event)

    notification_message = f"A section titled '{instance.name}' has been {'created' if created else 'updated'} for the event '{event.name}'."

    for participant in participants:
        notification = Notification.objects.create(
            user=participant.user, message=notification_message
        )


@receiver(post_save, sender=Participant)
def notification_for_adding_participant(sender, instance, created, **kwargs):
    notification_message = (
        f"Your Are Join Successfully to {instance.event.name}, enjoy it."
    )
    if created:
        Notification.objects.create(user=instance.user, message=notification_message)


@receiver(post_save, sender=WaitingList)
def notification_for_adding_participant(sender, instance, created, **kwargs):
    notification_message = (
        f"Your Are Adding into Waiting List for  {instance.event.name} event."
    )
    if created:
        Notification.objects.create(user=instance.user, message=notification_message)


