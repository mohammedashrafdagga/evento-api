from django.core.management.base import BaseCommand
from apps.events.models import Category, Event, Section
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Populate events and Section model with examples"

    def handle(self, *args, **kwargs):
        fake = Faker()
        user = User.objects.filter(username="wetest").first()
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
        for _ in range(10):
            category = random.choice(categories)
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
