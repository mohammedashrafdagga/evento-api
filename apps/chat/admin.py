from django.contrib import admin
from .models import EventGroupMessage, UserGroupMessage

# Message Admin Panel
class EventGroupMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "event__name", "text_content", "create_at")
    list_filter = ("sender", "event__name", "create_at")


admin.site.register(EventGroupMessage, EventGroupMessageAdmin)


# Message Admin Panel
class UserGroupMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver__username", "create_at")
    list_filter = ("sender", "receiver__username", "create_at")


admin.site.register(UserGroupMessage, UserGroupMessageAdmin)
