from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('messages_page/', consumers.ChatConsumer.as_asgi()),
]