from django.contrib import admin

from .models import (
    EventGroupMessage,
    EventMessage,
    Message,
    UserGroupMessage,
    UserMessage,
)


#  register Message Model
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "text_content")


admin.site.register(Message, MessageAdmin)

# register Event Message Model
class EventMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event__id",
    )


admin.site.register(EventMessage, EventMessageAdmin)


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


# register New User Model
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ("sender__username", "receiver__username")


admin.site.register(UserMessage, UserMessageAdmin)
