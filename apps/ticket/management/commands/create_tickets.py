import random
from apps.ticket.models import Ticket
from apps.events.models import Event
from faker import Faker

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create random tickets for all events with random prices."

    def handle(self, *args, **kwargs):
        faker = Faker()
        events = Event.objects.all()

        for event in events:
            price = round(random.uniform(10.99, 99.99), 2)
            marketing_sentence = faker.catch_phrase()
            ticket_name = f"{marketing_sentence} - {event.name}"
            max_user = random.randint(100, 1000)
            Ticket.objects.create(
                title=ticket_name, event=event, ticket_price=price, max_user=max_user
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Ticket created for event {event.id} with price {price}"
                )
            )
        self.stdout.write(self.style.SUCCESS("All tickets created successfully!"))
