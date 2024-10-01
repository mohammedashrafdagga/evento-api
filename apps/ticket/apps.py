from django.apps import AppConfig


class TicketConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ticket"

    def ready(self) -> None:
        import apps.ticket.signals
