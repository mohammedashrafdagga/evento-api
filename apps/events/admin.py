from django.contrib import admin

from .models import Event, Section, Participant, WaitingList

# Register your models here.

# Section Model
class SectionInlineAdmin(admin.TabularInline):
    model = Section
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "event__name",
        "speaker",
        "location",
        "start_datetime",
        "end_datetime",
    )
    search_fields = (
        "name",
        "event__name",
        "start_datetime",
        "end_datetime",
        "location",
    )
    list_filter = ("name", "speaker")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "availability",
        "host",
        "location",
        "start_date",
        "end_date",
    )
    search_fields = (
        "name",
        "availability",
        "host__username",
        "start_date",
        "end_date",
        "location",
    )
    list_filter = ("name", "availability", "location")
    inlines = [SectionInlineAdmin]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "event__name", "event__id", "user__username", "join_datetime")
    search_fields = ("event__name", "user__username", "join_datetime")
    list_filter = ("event__name", "user__username")


# WaitingList
@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event__name",
        "event__id",
        "user__username",
        "request_datetime",
    )
    search_fields = ("event__name", "user__username", "request_datetime")
    list_filter = ("event__name", "user__username")
