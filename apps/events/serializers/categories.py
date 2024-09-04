from apps.events.models import Event, Category
from rest_framework import serializers
from .events import event_fields


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = event_fields


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    events = EventCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "events"]
