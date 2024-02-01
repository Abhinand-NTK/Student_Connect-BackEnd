

from django.urls import re_path
from blog.consumers import NotificationConsumer


# websocket_urlpatterns = [
#     re_path(r'ws/notifications/$',NotificationConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', NotificationConsumer.as_asgi()),
]