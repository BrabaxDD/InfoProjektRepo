"""
ASGI config for Infoproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import game.routing
import game.consumers
from django.urls import re_path
import Infoproject.routing
from channels.generic.websocket import WebsocketConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Infoproject.settings")
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": Infoproject.routing.router
})
