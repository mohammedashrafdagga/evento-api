from django.db import models
from django.contrib.auth import get_user_model
from apps.events.models import Event
import uuid

# initialize User
User = get_user_model()

# Ticketing Model
class Ticket(models.Model):
    #  We have Some Contains
    title = models.CharField(max_length=255)
    slug = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    event = models.OneToOneField(
        Event, related_name="tickets", null=True, blank=True, on_delete=models.SET_NULL
    )
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    max_user = models.PositiveIntegerField(default=1000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Ticket for Event: {self.event.name} - {self.title[:20]}"


# Ticket Seller Model for User Buy Model
class TicketSeller(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name="ticket_seller", on_delete=models.CASCADE
    )
    buyer = models.ForeignKey(
        User, related_name="buyer", on_delete=models.SET_NULL, null=True, blank=True
    )

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Ticket for Event: {self.ticket.event.name[:20]} Buy By {self.buyer}"
