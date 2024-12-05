from django.urls import re_path
from channels.routing import URLRouter
from .consumers import gameServer

app = gameServer.gameServer.as_asgi()
