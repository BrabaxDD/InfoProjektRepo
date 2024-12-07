from channels.generic.websocket import WebsocketConsumer
import json
import random
from asgiref.sync import async_to_sync
from game.consumers import serverThreat
import threading


class gameServer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.tmpGroupName = "test"
        self.running = False
        self.serverThreat = serverThreat.serverThreat("test", 1000, self)

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.tmpGroupName, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.running = False
        pass

    def receive(self, text_data):
        if not self.running:
            self.running = True
            self.serverThreat.start()
        data_json = json.loads(text_data)
        self.send(json.dumps(
            {"positionx": random.random()*100,
             "positiony": random.random()*100
             }))

    def update(self):

        self.send(json.dumps(
            {"posx": 10,
             "posy": 10
             }))

    def getRunning(self):
        return self.running
