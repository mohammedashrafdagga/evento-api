from apps.events.models import Event, Participant
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Migrate participants from Event.user_participants to the Participant model"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting participant migration..."))
        migrated_count = 0
        events = Event.objects.all()
        for event in events:
            for user in event.user_participants.all():
                Participant.objects.create(user=user, event=event)
                migrated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully migrated {migrated_count} participants!")
        )
