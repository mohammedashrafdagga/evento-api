from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TicketSeller
from apps.events.models import Participant


@receiver(post_save, sender=TicketSeller)
def create_ticket_seller(sender, instance, created, **kwargs):
    Participant.objects.create(event=instance.ticket.event, user=instance.buyer)
