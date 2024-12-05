from channels.routing import URLRouter
from django.urls import re_path
import game.routing
router = URLRouter([re_path("game/",game.routing.app)])
