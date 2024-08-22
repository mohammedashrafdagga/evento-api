from django.contrib import admin

from .models import Event, Section

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
    list_display = ("id", "name", "host", "location", "start_date", "end_date")
    search_fields = ("name", "host__username", "start_date", "end_date", "location")
    list_filter = ("name", "location")
    inlines = [SectionInlineAdmin]
