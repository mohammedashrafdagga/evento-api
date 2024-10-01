from rest_framework import serializers
from .models import Ticket, TicketSeller
from apps.authentication.serializers import UserInfoSerializer


class TicketSellerSerializer(serializers.ModelSerializer):
    buyer = UserInfoSerializer(read_only=True)

    class Meta:
        model = TicketSeller
        fields = "__all__"
        read_only_fields = ["ticket"]


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "slug",
            "event",
            "ticket_price",
            "create_at",
        ]


class TicketSerializer(serializers.ModelSerializer):
    ticket_sellers = serializers.SerializerMethodField()  # Custom method for sellers
    user_count = (
        serializers.SerializerMethodField()
    )  # Count of users who bought tickets
    total_price = serializers.SerializerMethodField()  # Count of total price

    class Meta:
        model = Ticket
        fields = [
            "title",
            "slug",
            "event",
            "ticket_price",
            "max_user",
            "create_at",
            "ticket_sellers",
            "user_count",
            "total_price",
        ]

    def get_ticket_sellers(self, obj):
        # Fetch all TicketSellers related to this ticket
        sellers = TicketSeller.objects.filter(ticket=obj)
        return TicketSellerSerializer(sellers, many=True).data

    def get_user_count(self, obj):
        #  Count the number of unique buyers for the ticket
        return (
            TicketSeller.objects.filter(ticket=obj).values("buyer").distinct().count()
        )

    def get_total_price(self, obj):
        # Calculate the total price for all tickets sold for this event
        # Assuming each TicketSeller instance corresponds to a ticket sold
        return TicketSeller.objects.filter(ticket=obj).count() * obj.ticket_price
