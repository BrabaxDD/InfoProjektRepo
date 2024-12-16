from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from game.consumers import serverThreat
import threading
from game.ServerClasses import jsonSerializer


class gameServer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.serverID = ""
        self.running = False
        self.serverThreat = serverThreat.serverThreat("test", 1000, self)

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.running = False
        pass

    def receive(self, text_data):
        print("log: received package to server websocket with ID " +
              str(self.serverID) + " and the following content:")
        print(text_data)

        data_json = json.loads(text_data)
        if data_json["type"] == "startserver":
            self.serverID = data_json["serverID"]
            if not self.running:
                self.running = True
                self.serverThreat.start()
                async_to_sync(self.channel_layer.group_add)(
                    self.serverID, self.channel_name)

    def updatePosition(self, ID, posx, posy, entityType):
        async_to_sync(self.channel_layer.group_send)(
            self.serverID,
            {"type": "position",
             "ID": ID,
             "posx": posx,
             "posy": posy,
             "entityType": entityType})

    def updateInventory(self, ID, Invetory):
        async_to_sync(self.channel_layer.group_send)(self.serverID,
                                                     {"type": "inventoryUpdate",
                                                      "ID": ID,
                                                      "Inventory": json.dumps(Invetory, default=jsonSerializer.asDict)
                                                      }
                                                     )

    def hitRequestFromClient(self, event):
        self.serverThreat.hitRequestFromPlayer(event["ID"],event["direction"])
        pass

    def generateItem(self, event):
        self.serverThreat.playerGenerateItem(event)

    def inventoryUpdate(self, event):
        pass

    def action(self, event):
        self.serverThreat.playerActionUpdate(event)
        pass

    def login(self, event):
        print("log: new Player logged in to server with ID: " +
              self.serverID + " the Player ID is: " + str(event["ID"]))
        self.serverThreat.login(event["ID"])

    def getRunning(self):
        return self.running

    def position(self, event):
        pass
