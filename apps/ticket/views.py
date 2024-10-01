from rest_framework import generics
from .serializers import TicketListSerializer, TicketSerializer, TicketSellerSerializer
from .models import Ticket, TicketSeller
from rest_framework.permissions import IsAuthenticated
from .permissions import OwnerEventTicketPermission, OwnerEventPermission
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from apps.events.models import Event
from rest_framework.exceptions import ValidationError


# Main list Serializer for Ticket
@extend_schema(tags=["Events-Ticket"])
class EventTicketAPIView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        event_id = int(self.kwargs["event_id"])
        return Ticket.objects.filter(event_id=event_id)


# Main list Serializer for Ticket
@extend_schema(tags=["Events-Ticket"])
class TicketRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, OwnerEventTicketPermission]

    def get_object(self):
        """
        Override get_object to retrieve the first ticket for a specific event_id
        """
        event_id = int(self.kwargs["event_id"])
        try:
            # Get the first ticket associated with the event_id
            ticket = Ticket.objects.filter(event__id=event_id).first()
            if not ticket:
                raise NotFound("No tickets found for this event.")

            self.check_object_permissions(self.request, ticket)

            return ticket
        except Ticket.DoesNotExist:
            raise NotFound("No tickets found for this event.")


@extend_schema(tags=["Events-Ticket"])
class EventCreateTicketAPIView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated, OwnerEventPermission]

    def perform_create(self, serializer):
        event_id = int(self.kwargs["event_id"])

        try:
            event = Event.objects.get(id=event_id)

            self.check_object_permissions(self.request, event)

            if Ticket.objects.filter(event=event).exists():
                raise ValidationError(
                    {"detail": "A ticket for this event already exists."}
                )

            return serializer.save(event=event)
        except Event.DoesNotExist:
            raise ValidationError(
                {"detail": f"Event with id {event_id} does not exist."}
            )


# Ticket Seller Buyer API View
class TicketSellerBuyerAPIView(generics.CreateAPIView):
    serializer_class = TicketSellerSerializer
    queryset = TicketSeller.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # get tickets
        ticket = self.get_ticket(slug=self.kwargs["slug"])
        # check ticket
        self.check_existing_ticket_seller(ticket=ticket)
        # Save the TicketSeller instance with the ticket and the buyer
        return serializer.save(ticket=ticket, buyer=self.request.user)

    def get_ticket(self, slug):
        """Return Ticket Object Using Slug"""
        try:
            return Ticket.objects.get(slug=slug)
        except Ticket.DoesNotExist:
            raise ValidationError(
                {"detail": f"Ticket with slug: {slug} does not exist."}
            )

    def check_existing_ticket_seller(self, ticket: Ticket) -> None:
        """
        Check if the user already has a TicketSeller for the given ticket.
        Raise a ValidationError if a TicketSeller exists for the user.
        """
        if TicketSeller.objects.filter(ticket=ticket, buyer=self.request.user).exists():
            raise ValidationError(
                {"detail": "You already have a TicketSeller for this ticket."}
            )
