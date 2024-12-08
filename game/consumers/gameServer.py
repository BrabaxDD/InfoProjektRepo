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

    def updatePosition(self, ID, posx, posy):
        async_to_sync(self.channel_layer.group_send)(
            self.tmpGroupName,
            {"type": "position",
             "ID": ID,
             "posx": posx,
             "posy": posy})
        pass

    def action(self, event):
        self.serverThreat.playerActionUpdate(event)
        pass

    def login(self, event):
        #        self.serverThreat.login(event["ID"])
        print("received loginrequest")
        print(event)
        pass

    def getRunning(self):
        return self.running

    def position(self, event):
        pass
