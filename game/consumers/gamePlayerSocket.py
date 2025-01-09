from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
import datetime


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
        True
#        print("log: received Package by client to " +
#              str(self.player_ID) + " with the following content:")
#        print(text_data)
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
                print("arrived at client")
                print(datetime.datetime.now())
                direction = text_data_json["direction"]
                async_to_sync(self.channel_layer.group_send)(self.serverID, {
                    "type": "hitRequestFromClient", "direction": direction, "ID": self.player_ID})
            elif actiontype == "interact":
                print("log: Player with ID " + str(self.player_ID) + " is trying to interact")
                async_to_sync(self.channel_layer.group_send)(self.serverID, {
                    "type": "interactionRequestFromClient", "playerID": self.player_ID})
        if messageType == "combineStacks":
            print("log: got request to combine stacks with the following content")
            print(text_data_json)
            if "stackID1" in text_data_json and "stackID2" in text_data_json:
                stackID1 = text_data_json["stackID1"]
                stackDI2 = text_data_json["stackID2"]
                async_to_sync(self.channel_layer.group_send)(self.serverID, {
                    "type": "combineStacksRequest",
                    "stackID1": stackID1,
                    "stackID2": stackDI2,
                    "playerID": self.player_ID
                })
            else:
                print("log: Player send invalid combine request")
        if messageType == "craft":
            print("log: got request to craft with the following content from client with ID: " + str(self.player_ID))
            recipe = text_data_json["recipe"]
            async_to_sync(self.channel_layer.group_send)(self.serverID, {
                "type": "craftChannel",
                "playerID": self.player_ID,
                "recipe": recipe
            }

            )

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
        #        print("log: sending position information to Player with ID: " + str(self.player_ID) + " from server with ID " + self.serverID + " the position is: " +
        #              str(event["posx"]) + " " + str(event["posy"]) + " the entity type is " + str(event["entityType"]) + " the entity ID is: " + str(event["ID"]))
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
        playerID = event["ID"]
        if playerID == self.player_ID:
            print("log: updating Player Inventory with player ID: " + str(self.player_ID) +
                  "for server with ID: " + str(self.serverID) + "and with content: ")
            print(event["Inventory"])
            self.send(text_data=json.dumps({"type": "InventoryUpdate",
                                            "ID": event["ID"], "Inventory":   json.loads(event["Inventory"])}))

    def newGameObject(self, event):
        print("log: sending information about new GameObject on Server with ID: " + str(self.serverID) + " to client with ID " +
              str(self.player_ID) + " the ID of the new Object is " + str(event["ID"]) + " the entity Type is " + event["entityType"])
        self.send(text_data=json.dumps(
            {"type": "newGameObject", "ID": event["ID"], "entityType": event["entityType"]}))
        pass

    def healthUpdate(self, event):
        print("log: sending information about new Health on Server with ID: " + str(self.serverID) + " to client with ID " + str(self.player_ID) +
              " the ID of the Updated Object is " + str(event["ID"]) + " the entityType is " + event["entityType"] + " the new hp is " + str(event["HP"]))
        self.send(text_data=json.dumps(
            {"type": "healthUpdate", "ID": event["ID"], "entityType": event["entityType"], "HP": event["HP"]}))

    def passLoginInformationChannel(self, event):
        playerID = event["playerID"]
        entityID = event["entityID"]
        entityType = event["entityType"]
        if playerID == self.player_ID:
            self.send(text_data=json.dumps(
                {"type": "newGameObject", "ID": entityID, "entityType": entityType}))
        print("log: sending information about new GameObject on Server with ID: " + str(self.serverID) + " to client with ID " +
              str(self.player_ID) + " the ID of the new Object is " + str(entityID) + " the entity Type is " + entityType)

        pass

    def broadcastGameObjectDeletedChannel(self, event):
        entityID = event["entityID"]
        entityType = event["entityType"]
        print("log: sendfing Information about deleted GameObject on Server with ID:" + str(self.serverID) + " to client with ID: " +
              str(self.player_ID) + " the deleted entity has the ID: " + str(entityID) + " and the type: " + str(entityType))
        self.send(text_data=json.dumps(
            {"type": "deletedGameObject",
                "entityID": entityID, "entityType": entityType}
        ))

        pass

    def broadcastWallInformationChannel(self, event):
        posx2 = event["posx2"]
        posy2 = event["posy2"]
        thickness = event["thickness"]
        wallID = event["wallID"]
        self.send(text_data=json.dumps(
            {"type": "wallInformation", "posx2": posx2, "posy2": posy2, "thickness": thickness, "wallID": wallID}))
        pass

    def combineStacksRequest(self, event):
        pass

    def craftChannel(self, event):
        pass

    def connectionRefused(self, event):
        playerID = event["playerID"]
        if playerID == self.player_ID:
            print(
                "log: sending connection denied message to client with ID: " + str(self.player_ID))
            self.send(text_data=json.dumps({"type": "connectionRefused"}))
            self.disconnect(0)

    def connectionAccepted(self, event):
        playerID = event["playerID"]
        if playerID == self.player_ID:
            print(
                "log: sending connection accepted message to client with ID: " + str(self.player_ID))
            self.send(text_data=json.dumps({"type": "connectionAccepted"}))
        pass
    def interactionRequestFromClient(self,event):
        pass
