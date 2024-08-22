import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Notification
from .serializers import NotificationSerializer


User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    # connect Notification Consumer
    async def connect(self):
        # self.user = self.scope["user"]
        # if self.user.is_authenticated:
        #     await self.channel_layer.group_add(self.user.username, self.channel_name)
        await self.accept()

    # disconnect
    async def disconnect(self, _):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.user.username, self.channel_name
            )

    # send notification
    async def send_notification(self, event):
        notifications = event["notifications"]
        await self.send(text_data=json.dumps({"notifications": notifications}))
