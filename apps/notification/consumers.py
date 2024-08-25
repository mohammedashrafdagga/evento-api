import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    # connect Notification Consumer
    async def connect(self):

        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user = await self.get_user(self.user_id)
        print(self.user)
        if self.user is None:
            await self.close()

        else:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

            # Fetch and send unread notifications
            await self.fetch_and_send_notifications()

    # disconnect
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages if necessary
        pass

    # send notification
    async def send_notification(self, event):
        notification = event["notification"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification",
                    "message": notification["message"],
                    "notification_type": notification["notification_type"],
                    "created_at": notification["create_at"],
                }
            )
        )

    # get User
    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    # Get Notification
    @database_sync_to_async
    def get_notifications(self):
        return Notification.objects.filter(user=self.user)

    # fetch Notification
    async def fetch_and_send_notifications(self):
        notifications = await self.get_notifications()
        serialized_notifications = NotificationSerializer(notifications, many=True).data
        await self.send(text_data=json.dumps(serialized_notifications))
