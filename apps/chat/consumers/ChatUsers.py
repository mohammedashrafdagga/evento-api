import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chat.models import UserGroupMessage
from django.contrib.auth import get_user_model
from apps.chat.serializers import UserGroupMessageSerializer
import base64
import uuid
from io import BytesIO
from PIL import Image
import os
from django.conf import settings

User = get_user_model()

# Message Group Chatting
class MessageUsersChatting(AsyncWebsocketConsumer):
    # connection get User and Group Events
    async def connect(self):

        # send message
        self.group_name = f"chat_user"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def close(self, code=None, reason=None):
        return self.channel_layer.group_discard(self.group_name, self.channel_name)

    # send message for the User Join into Group or Event
    async def send_message(self, event):
        message = event["message"]
        serializer_data = UserGroupMessageSerializer(message).data
        await self.send(
            text_data=json.dumps({"action": "new_message", "messages": serializer_data})
        )

    # receive Message
    async def receive(self, text_data):

        data = json.loads(text_data)
        sender_id = int(data["sender_id"])
        receiver_id = int(data["receiver_id"])
        if data["action"] == "fetch_messages":

            sender_user = await self.get_user_by_id(sender_id)
            receiver_user = await self.get_user_by_id(receiver_id)
            if not sender_user and not receiver_user:
                return

            await self.get_chat_messages(sender=sender_user, receiver=receiver_user)
        else:

            sender_user = await self.get_user_by_id(sender_id)
            receiver_user = await self.get_user_by_id(receiver_id)
            if not sender_user and not receiver_user:
                return

            message = data["message"]
            image_base64 = data["image"]
            image_path = None

            if image_base64:
                try:
                    image_data = base64.b64decode(image_base64.split(",")[1])
                    image = Image.open(BytesIO(image_data))

                    # create a unique
                    image_filename = (
                        f"{sender_user.id}-{receiver_user}-{uuid.uuid4()}_image.png"
                    )
                    image_path = os.path.join("chat_users_images/", image_filename)
                    image_abs_path = os.path.join(settings.MEDIA_ROOT, image_path)
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(image_abs_path), exist_ok=True)

                    # save image
                    image.save(image_abs_path)
                except Exception as e:
                    print(f"Error saving image: {e}")
                    return
            # create Message
            await self.create_message_users(
                sender=sender_user,
                receiver=receiver_user,
                message=message,
                image=image_path,
            )

    @database_sync_to_async
    def get_user_by_id(self, user_id: int) -> User:
        try:
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            return None

    async def get_chat_messages(self, sender: User, receiver: User):
        users = [sender, receiver]
        messages = UserGroupMessage.objects.filter(sender__in=users, receiver__in=users)
        serializer_data = UserGroupMessageSerializer(messages, many=True).data

        await self.send(
            text_data=json.dumps(
                {"action": "previous_messages", "messages": serializer_data}
            )
        )

    @database_sync_to_async
    def create_message_users(self, sender: User, receiver: User, message: str, image):
        UserGroupMessage.objects.create(
            sender=sender, receiver=receiver, text_content=message, image_content=image
        )
