from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.TextRoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})

 