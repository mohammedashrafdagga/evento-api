import random

from apps.events.models import Category, Event, Section
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "Populate events and Section model with examples"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()
        
        if not users:
            self.stdout.write(
                self.style.WARNING(
                    "No users found. Please create users first."
                )
            )
            return
        # Assuming categories are already created
        categories = list(Category.objects.all())

        if not categories:
            self.stdout.write(
                self.style.WARNING(
                    "No categories found. Please create categories first."
                )
            )
            return

        # Create 10 Events
        for _ in range(10000):
            category = random.choice(categories)
            user = random.choice(users)
            event = Event.objects.create(
                host=user,
                name=fake.catch_phrase(),
                description=fake.paragraph(),
                start_date=fake.date_time_this_year(),
                end_date=fake.date_time_this_year(),
                location=fake.address(),
                category=category,
                availability=random.choice(["all", "specific"]),
            )

            # Create 2-5 Sections for each event
            for _ in range(random.randint(2, 5)):
                Section.objects.create(
                    event=event,
                    name=fake.catch_phrase(),
                    description=fake.paragraph(),
                    start_datetime=fake.date_time_this_year(),
                    end_datetime=fake.date_time_this_year(),
                    location=fake.address(),
                    speaker=fake.name(),
                )

            self.stdout.write(
                self.style.SUCCESS(f"Successfully populated event - {event.id}!")
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated Events!"))
