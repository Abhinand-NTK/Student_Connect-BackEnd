

from django.urls import re_path
from blog.consumers import NotificationConsumer,ActiveUserConsumer
from chat_messages.consumers import ChatConsumer
# from chat_messages.consumers import ChatConsumer


# websocket_urlpatterns = [
#     re_path(r'ws/notifications/$',NotificationConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/active_users/', ActiveUserConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]