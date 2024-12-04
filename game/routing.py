from django.urls import re_path

from .consumers import gameServer

websocket_urlpatterns = [re_path("ws/server", gameServer.gameServer.as_asgi())]
