from django.contrib import admin
from .models import Notification

# Register your models here.


@admin.register(Notification)
class Notification(admin.ModelAdmin):
    list_display = (
        "user__username",
        "message",
        "notification_type",
        "status",
        "create_at",
    )
    list_filter = ["notification_type", "status"]
    search_fields = ("user__username", "message", "notification_type")
