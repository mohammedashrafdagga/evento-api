from django.test import TestCase
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from .routers import chat_websocket_urlpatterns
from channels.routing import URLRouter
import asyncio
import json
from apps.events.models import Event, Category


# Create your tests here.
User = get_user_model()


# test consumer
class MessageGroupChattingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", password="testuser@admin.com"
        )
        self.category = Category.objects.create(name="Finance")
        self.event = Event.objects.create(
            host=self.user,
            name="testuser",
            category=self.category,
            description="test description",
            location="Gaza",
            start_date="2018-04-04",
            end_date="2018-04-05",
            availability="all",
        )

    async def test_connect(self):
        try:

            application = URLRouter(chat_websocket_urlpatterns)
            communicator = WebsocketCommunicator(application, f"/we/chat/group/1/")

            communicator.scope["user_id"] = self.user.id
            connected, subprotocol = await communicator.connect()
            self.assertTrue(connected)

            # response data
            response = await communicator.receive_from()

            print(response)

            await communicator.disconnect()
        except asyncio.TimeoutError:
            self.fail("WebSocket connection timed out")
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")
