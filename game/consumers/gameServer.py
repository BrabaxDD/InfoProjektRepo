from channels.generic.websocket import WebsocketConsumer
import json
import random


class gameServer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.tmpGroupName = "test"

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.send(json.dumps(
            {"positionx": random.random()*100,
             "positiony": random.random()*100
             }))
