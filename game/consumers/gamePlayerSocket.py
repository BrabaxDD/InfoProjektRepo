from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class gamePlayerSocketConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.firstMessage = True
        self.gameServerName = ""
        self.player_ID = "opfer"
        self.serverID = ""

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
        async_to_sync(self.channel_layer.group_discard)(
            self.serverID, self.channel_name)

    def receive(self, text_data):
        print("log: received Package by client to " +
              str(self.player_ID) + " with the following content:")
        print(text_data)
        text_data_json = json.loads(text_data)
        messageType = text_data_json["type"]
        if messageType == "action":
            actiontype = text_data_json["actiontype"]

            if actiontype == "movement":
                up = text_data_json["up"]
                down = text_data_json["down"]
                left = text_data_json["left"]
                right = text_data_json["right"]

                async_to_sync(self.channel_layer.group_send)(
                    self.serverID,
                    {
                        "type": "action",
                        "ID": self.player_ID,
                        "up": up,
                        "down": down,
                        "left": left,
                        "right": right,
                    }
                )
            elif actiontype == "hit":
                direction = text_data_json["direction"]
                async_to_sync(self.channel_layer.group_send)(self.serverID, {
                    "type": "hitRequestFromClient", "direction": direction, "ID": self.player_ID})

        if messageType == "login":
            ID = text_data_json["ID"]
            serverID = text_data_json["serverID"]
            self.serverID = serverID
            async_to_sync(self.channel_layer.group_add)(
                self.serverID, self.channel_name)
            self.player_ID = ID
            async_to_sync(self.channel_layer.group_send)(
                self.serverID, {"type": "login", "ID": ID})
#            self.send(text_data=json.dumps({"type":"loginSucessfull"}))
        if messageType == "generateItem":
            itemID = text_data_json["itemID"]
            async_to_sync(self.channel_layer.group_send)(
                self.serverID, {"type": "generateItem", "itemID": itemID, "ID": self.player_ID})
            print("log: Got generateItem Request from client with ID: " + self.player_ID +
                  "giving it to server with ID: " + self.serverID + "giving it to server with ID: " + self.serverID + " the content is: ")
            print(text_data_json)

    def hitRequestFromClient(self, event):
        pass

    def position(self, event):
        #print("log: sending position information to Player with ID: " + str(self.player_ID) + " from server with ID " + self.serverID + " the position is: " +
        #      str(event["posx"]) + " " + str(event["posy"]) + " the entity type is " + str(event["entityType"]) + " the entity ID is: " + str(event["ID"]))
        posx = event["posx"]
        posy = event["posy"]
        ID = event["ID"]
        entityType = event["entityType"]
        self.send(text_data=json.dumps({
            "type": "position",
            "ID": ID,
            "posx": posx,
            "posy": posy,
            "entityType": entityType
        }))

    def generateItem(self, event):
        pass

    def login(self, event):
        pass

    def action(self, event):
        pass

    def inventoryUpdate(self, event):
        print("log: updating Player Inventory with player ID: " + self.player_ID +
              "for server with ID: " + self.serverID + "and with content: ")
        print(event["Inventory"])
        self.send(text_data=json.dumps({"type": "InventoryUpdate",
                                        "ID": event["ID"], "Inventory": event["Inventory"]}))
