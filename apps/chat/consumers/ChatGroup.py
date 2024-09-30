import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chat.models import EventGroupMessage
from apps.events.models import Event
from django.contrib.auth import get_user_model
from apps.chat.serializers import EventGroupMessageSerializer
import base64
import uuid
from io import BytesIO
from PIL import Image
import os
from django.conf import settings

User = get_user_model()

# Message Group Chatting
class MessageGroupChatting(AsyncWebsocketConsumer):
    # connection get User and Group Events
    async def connect(self):

        event_id = int(self.scope["url_route"]["kwargs"]["event_id"])
        event = await self.get_event_by_id(event_id=event_id)

        if not event:
            self.close()

        # send message
        self.group_name = f"event_group_{event_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def close(self, code=None, reason=None):
        return self.channel_layer.group_discard(self.group_name, self.channel_name)

    # send message for the User Join into Group or Event
    async def send_message(self, event):
        message = event["message"]
        serializer_data = EventGroupMessageSerializer(message).data
        await self.send(
            text_data=json.dumps(
                {
                    "action": "new_message",
                    "messages": serializer_data,
                }
            )
        )

    # receive Message
    async def receive(self, text_data):
        event_id = int(self.scope["url_route"]["kwargs"]["event_id"])
        event = await self.get_event_by_id(event_id=event_id)
        if not event:
            return

        data = json.loads(text_data)

        if data["action"] == "fetch_messages":
            await self.get_events_message(event=event)
        else:
            sender_id = data["sender_id"]
            sender = await self.get_user_by_id(user_id=sender_id)
            if not sender:
                return

            if event.host != sender:
                return

            # message and image
            image_base64 = data["image"]
            message = data["message"]
            image_path = None
            if image_base64:
                try:
                    # Decode the base64 image data
                    image_data = base64.b64decode(image_base64.split(",")[1])
                    image = Image.open(BytesIO(image_data))

                    # Create a unique filename
                    image_filename = f"{event.id}-{uuid.uuid4()}_image.png"
                    image_path = os.path.join("chat_group_images/", image_filename)
                    image_abs_path = os.path.join(settings.MEDIA_ROOT, image_path)
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(image_abs_path), exist_ok=True)

                    # Save the image to the media directory
                    image.save(image_abs_path)

                except Exception as e:
                    print(f"Error saving image: {e}")
                    return

            # create Message
            await self.create_event_message(
                event=event, image=image_path, message=message, sender=sender
            )

    @database_sync_to_async
    def get_user_by_id(self, user_id: int) -> User:
        try:
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            return None

    @database_sync_to_async
    def get_event_by_id(self, event_id: int) -> Event:
        try:
            event = Event.objects.get(id=event_id)
            return event
        except Exception as e:
            print("The error is: ", e)
            return None

    async def get_events_message(self, event: Event):
        messages = EventGroupMessage.objects.filter(event=event)
        serializer_data = EventGroupMessageSerializer(messages, many=True).data
        print(serializer_data)
        await self.send(
            text_data=json.dumps(
                {
                    "action": "previous_messages",
                    "messages": serializer_data,
                }
            )
        )

    @database_sync_to_async
    def create_event_message(self, event: Event, sender: User, message: str, image):

        EventGroupMessage.objects.create(
            event=event, sender=sender, text_content=message, image_content=image
        )
