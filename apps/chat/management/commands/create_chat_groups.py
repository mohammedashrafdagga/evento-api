from django.core.management import BaseCommand
from apps.chat.models import ChatGroup
from apps.events.models import Event


class Command(BaseCommand):
    help = "Create a chat group for all events that do not have one"

    def handle(self, *args, **options):
        events_without_chat_groups = Event.objects.filter(chat_group__isnull=True)
        for event in events_without_chat_groups:
            ChatGroup.objects.create(name=f"Chat for {event.name}", event=event)
            self.stdout.write(
                self.style.SUCCESS(f"Chat group created for event: {event.name}")
            )
        if not events_without_chat_groups:
            self.stdout.write(
                self.style.SUCCESS("All events already have a chat group.")
            )

        self.stdout.write(
            self.style.SUCCESS("Creating Group for All events is Finished.")
        )
