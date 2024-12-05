from channels.generic.websocket import WebsocketConsumer
import json


class gamePlayerSocketConsumer(WebsocketConsumer):
    def __init__(self):
        self.firstMessage = True
        self.gameServerName = ""
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
         if self.firstMessage:
            text_data_json = json.loads(text_data)
            self.gameServerName = text_data_json["serverName"]


        self.send(json.dumps({"positionx": 200, "positiony": 200}))
