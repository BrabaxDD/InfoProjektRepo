from django.urls import re_path
from channels.routing import URLRouter
from .consumers import gameServer, gamePlayerSocket

app = URLRouter([re_path("", gameServer.gameServer.as_asgi()),
                 # re_path("", gamePlayerSocket.gamePlayerSocketConsumer.as_asgi())
                 ])