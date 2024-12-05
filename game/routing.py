from django.urls import re_path
from channels.routing import URLRouter
from .consumers import gameServer, gamePlayerSocket

app = URLRouter([re_path("server", gameServer.gameServer.as_asgi()), re_path(
    "login", gamePlayerSocket.gamePlayerSocketConsumer.as_asgi())])
