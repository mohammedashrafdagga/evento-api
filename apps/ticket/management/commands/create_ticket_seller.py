import random
from django.core.management.base import BaseCommand
from apps.ticket.models import TicketSeller, Ticket
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Create a new TicketSeller"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        tickets = Ticket.objects.all()

        if not users.exists():
            self.stdout.write(
                self.style.ERROR("No users found. Please create some users first.")
            )
            return

        if not tickets.exists():
            self.stdout.write(
                self.style.ERROR("No tickets found. Please create some tickets first.")
            )
            return

        for ticket in tickets:
            num_sellers = random.randint(1, 5)
            for _ in range(num_sellers):
                buyer = random.choice(
                    users
                )  # Randomly select a buyer from the user list
                TicketSeller.objects.create(ticket=ticket, buyer=buyer)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'TicketSeller created for ticket "{ticket.title}", buyer {buyer.username}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("All ticket sellers created successfully!")
        )
