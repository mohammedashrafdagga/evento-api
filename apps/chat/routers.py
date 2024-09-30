from django.urls import re_path
from apps.chat.consumers.ChatGroup import MessageGroupChatting
from apps.chat.consumers.ChatUsers import MessageUsersChatting


chat_websocket_urlpatterns = [
    re_path(
        r"^ws/chat/events/(?P<event_id>\d+)/$",
        MessageGroupChatting.as_asgi(),
    ),
    re_path(
        r"^ws/chat/users/$",
        MessageUsersChatting.as_asgi(),
    ),
]
