from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from game.consumers import serverThreat
import threading


class gameServer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.running = False
        self.serverThreat = serverThreat.serverThreat("test", 1000, self)

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.running = False
        pass

    def receive(self, text_data):
        print("log: received package to server websocket with name " +
              str(self.name) + " and the following content:")
        print(text_data)

        data_json = json.loads(text_data)
        if data_json["type"] == "startserver":
            self.name = data_json["name"]
            if not self.running:
                self.running = True
                self.serverThreat.start()
                async_to_sync(self.channel_layer.group_add)(
                    self.name, self.channel_name)

    def updatePosition(self, ID, posx, posy):
        async_to_sync(self.channel_layer.group_send)(
            self.name,
            {"type": "position",
             "ID": ID,
             "posx": posx,
             "posy": posy})
        pass

    def action(self, event):
        self.serverThreat.playerActionUpdate(event)
        pass

    def login(self, event):
        self.serverThreat.login(event["ID"])

    def getRunning(self):
        return self.running

    def position(self, event):
        pass
