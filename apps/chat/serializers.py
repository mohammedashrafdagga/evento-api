from rest_framework import serializers
from .models import EventGroupMessage, UserGroupMessage


class EventGroupMessageSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    image_content = serializers.SerializerMethodField()

    class Meta:
        model = EventGroupMessage
        fields = (
            "host",
            "event",
            "text_content",
            "image_content",
            "create_at",
        )

    def get_host(self, obj):
        return obj.sender.username

    def get_image_content(self, obj):
        if obj.image_content and hasattr(obj.image_content, "url"):
            return obj.image_content.url
        return None


class UserGroupMessageSerializer(serializers.ModelSerializer):
    sender_user = serializers.SerializerMethodField()
    receiver_user = serializers.SerializerMethodField()
    image_content = serializers.SerializerMethodField()

    class Meta:
        model = UserGroupMessage
        fields = (
            "sender_user",
            "receiver_user",
            "text_content",
            "create_at",
            "image_content",
            "is_read",
        )

    # receiver username
    def get_receiver_user(self, obj):
        return obj.receiver.username

    # sender username
    def get_sender_user(self, obj):
        return obj.sender.username

    def get_image_content(self, obj):
        if obj.image_content and hasattr(obj.image_content, "url"):
            return obj.image_content.url
        return None
