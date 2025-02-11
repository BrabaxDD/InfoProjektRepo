from channels.generic.websocket import WebsocketConsumer
import json
import datetime
from asgiref.sync import async_to_sync
from game.consumers import serverThreat
import threading
from game.ServerClasses import jsonSerializer
from game.models import runningServers
import time


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
        serverDB = runningServers.objects.get(serverID=self.serverID)
        serverDB.delete()
#        with open("tmp/runningservers.txt", "r") as file:
#            lines = file.readlines()
#        with open("tmp/runningservers.txt", "w") as file:
#            for line in lines:
#                if self.serverID not in line:
#                    file.write(line)
#        pass

    def broadcastDeadPlayer(self, playerID):
        async_to_sync(self.channel_layer.group_send)(self.serverID,
                                                     {"type": "deadPlayerChannel",
                                                      "playerID": playerID,
                                                      }
                                                     )

    def receive(self, text_data):
        print("log: received package to server websocket with ID " +
              str(self.serverID) + " and the following content:")
        print(text_data)

        data_json = json.loads(text_data)
        alreadyExisting = False
        if data_json["type"] == "startserver":
            self.serverID = data_json["serverID"]
            alreadyRunning = False
            for server in runningServers.objects.all():
                if server.serverID == self.serverID:
                    print(
                        "log: someone is trying to start a server wich aleready runns")
                    alreadyRunning = True
            if not alreadyRunning:
                serverDB = runningServers.objects.create(
                    serverID=self.serverID)
                self.running = True
                self.serverThreat.start()
                self.send(text_data=json.dumps({"type":"serverReadyForPlayer"}))
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

    def updateHealth(self, ID, entityType, HP):
        async_to_sync(self.channel_layer.group_send)(self.serverID, {
            "type": "healthUpdate", "ID": ID, "entityType": entityType, "HP": HP})

    def broadcastNewObject(self, entityType, ID):
        async_to_sync(self.channel_layer.group_send)(self.serverID, {
            "type": "newGameObject", "ID": ID, "entityType": entityType})

    # send new game Object information only to new player
    def passLoginInformation(self, playerID, entityType, entityID):
        async_to_sync(self.channel_layer.group_send)(self.serverID, {
            "type": "passLoginInformationChannel",
            "playerID": playerID,
            "entityType": entityType,
            "entityID": entityID
        })

    def broadcastGameObjectDeleted(self, entityType, entityID):
        async_to_sync(self.channel_layer.group_send)(self.serverID, {
            "type": "broadcastGameObjectDeletedChannel",
            "entityType": entityType,
            "entityID": entityID,
        })

    def broadcastGameObjectDeletedChannel(self, event):
        pass

    def broadcastWallInformation(self, posx2, posy2, thickness, wallID):
        async_to_sync(self.channel_layer.group_send)(self.serverID, {
            "type": "broadcastWallInformationChannel",
            "posx2": posx2,
            "posy2": posy2,
            "thickness": thickness,
            "wallID": wallID
        })

    def broadcastWallInformationChannel(self, event):
        pass

    def hitRequestFromClient(self, event):
        print("received Hit Request from Client " + str(time.time()))
        self.serverThreat.hitRequestFromPlayer(event["ID"], event["direction"])
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

    def respondToLogin(self, accepted, playerID):
        if accepted:
            async_to_sync(self.channel_layer.group_send)(self.serverID, {
                "type": "connectionAccepted", "playerID": playerID})
        else:
            async_to_sync(self.channel_layer.group_send)(self.serverID, {
                "type": "connectionRefused", "playerID": playerID})

    def getRunning(self):
        return self.running

    def position(self, event):
        pass

    def passLoginInformationChannel(self, event):
        pass

    def newGameObject(self, event):
        pass

    def healthUpdate(self, event):
        pass

    def combineStacksRequest(self, event):
        stackID1 = event["stackID1"]
        stackID2 = event["stackID2"]
        playerID = event["playerID"]
        self.serverThreat.requestItemStackCombination(
            stackID1, stackID2, playerID)
        pass

    def craftChannel(self, event):
        recipe = event["recipe"]
        playerID = event["playerID"]
        self.serverThreat.requestCraft(recipe, playerID)
        pass

    def connectionRefused(self, event):
        pass

    def connectionAccepted(self, event):
        pass

    def interactionRequestFromClient(self, event):
        playerID = event["playerID"]
        self.serverThreat.interactionRequestFromPlayer(playerID)
        pass

    def setHotbar(self, event):
        stackID = event["stackID"]
        hotbarSlot = event["hotbarSlot"]
        playerID = event["playerID"]
        self.serverThreat.setHotbarRequest(playerID, hotbarSlot, stackID)
        pass

    def setActiveSlot(self, event):
        playerID = event["playerID"]
        slot = event["slot"]
        self.serverThreat.world.eventBus.event(
            "setActiveSlot", {"playerID": playerID, "slot": slot})
        pass

    def deadPlayerChannel(self, event):
        pass

    def respawnPlayerChannels(self, event):
        playerID = event["playerID"]
        self.serverThreat.world.eventBus.event(
            "respawnPlayer", {"playerID": playerID})
