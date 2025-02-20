from channels.generic.websocket import WebsocketConsumer
import json
import datetime
from asgiref.sync import async_to_sync
from game.consumers import serverThread
import threading
from game.ServerClasses import jsonSerializer
from game.models import runningServers
import time


class gameServer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.serverID = ""
        self.running = False
        self.serverThread = serverThread.serverThread("test", 1000, self)

    '''Hier die Standartfunktionen des Websockets'''
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.running = False
        serverDB = runningServers.objects.get(serverID=self.serverID)
        serverDB.delete()

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
                    print("log: someone is trying to start a server wich aleready runns")
                    alreadyRunning = True
            if not alreadyRunning:
                serverDB = runningServers.objects.create(serverID=self.serverID)
                self.running = True
                self.serverThread.start()
                self.send(text_data=json.dumps({"type":"serverReadyForPlayer"}))
                async_to_sync(self.channel_layer.group_add)(f"server_{self.serverID}", self.channel_name)



    def respondToLogin(self, accepted, playerID):
        if accepted:
            async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
                "type": "connectionAccepted", "playerID": playerID})
        else:
            async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
                "type": "connectionRefused", "playerID": playerID})


    def getRunning(self):
        return self.running
    '''Hier kommen die async_to_sync funktionen hin. Das type:feld bezeichnet die Funktion,
    die sowohl in dieser Klasse, als auch in dem gamePlayerSocket ausgeführt werden. Das liegt 
    (glaube ich) an den group_send, weil die Gruppe falsch eingstellt ist.'''

    '''Jedes mal, wenn einer der beiden Websockets eine Funktion ausführt, (mit dem send), dann wird es auf beiden ausgeführt.
    Deshalb sind unten so viele leere Funktionn. Die Unterscheidung in GameServer und GamePLayerSocket ist für das Frontend.'''

    '''Das sind praktisch die Funktionen, die nach außen/zum Frontend gehen'''


    def broadcastDeadPlayer(self, playerID):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}",
                                                     {"type": "deadPlayerChannel",
                                                      "playerID": playerID,
                                                      }
                                                     )

    def updatePosition(self, ID, posx, posy, entityType):
        async_to_sync(self.channel_layer.group_send)(
            f"player_{self.serverID}",
            {"type": "position",
             "ID": ID,
             "posx": posx,
             "posy": posy,
             "entityType": entityType})

    def updateInventory(self, ID, Invetory):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}",
                                                     {"type": "inventoryUpdate",
                                                      "ID": ID,
                                                      "Inventory": json.dumps(Invetory, default=jsonSerializer.asDict)
                                                      }
                                                     )

    def updateHealth(self, ID, entityType, HP):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
            "type": "healthUpdate", "ID": ID, "entityType": entityType, "HP": HP})

    def broadcastNewObject(self, entityType, ID):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
            "type": "newGameObject", "ID": ID, "entityType": entityType})

    # send new game Object information only to new player
    def passLoginInformation(self, playerID, entityType, entityID):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
            "type": "passLoginInformationChannel",
            "playerID": playerID,
            "entityType": entityType,
            "entityID": entityID
        })

    def broadcastGameObjectDeleted(self, entityType, entityID):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
            "type": "broadcastGameObjectDeletedChannel",
            "entityType": entityType,
            "entityID": entityID,
        })


    def broadcastWallInformation(self, posx2, posy2, thickness, wallID):
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
            "type": "broadcastWallInformationChannel",
            "posx2": posx2,
            "posy2": posy2,
            "thickness": thickness,
            "wallID": wallID
        })

    def testMessage(self):
        print("Sending Test message")
        async_to_sync(self.channel_layer.group_send)(f"player_{self.serverID}", {
            "type": "testMessageSocket",
            "text": "WOW,TEXT!"
        })



    '''Ab hier sind praktisch Funktionen, die nach innen / ins backend gehen und vom gamePlayerSocket ausgelöst werden.
    Diese werden also vom Frontend ausgelöst.'''

    def hitRequestFromClient(self, event):
        print("received Hit Request from Client " + str(time.time()))
        self.serverThread.hitRequestFromPlayer(event["ID"], event["direction"])
        pass

    def generateItem(self, event):
        self.serverThread.playerGenerateItem(event)


    def action(self, event):
        self.serverThread.playerActionUpdate(event)
        pass

    def login(self, event):
        print("log: new Player logged in to server with ID: " +
              self.serverID + " the Player ID is: " + str(event["ID"]))
        self.serverThread.login(event["ID"])

 
    def combineStacksRequest(self, event):
        stackID1 = event["stackID1"]
        stackID2 = event["stackID2"]
        playerID = event["playerID"]
        self.serverThread.requestItemStackCombination(
            stackID1, stackID2, playerID)
        pass

    def craftChannel(self, event):
        recipe = event["recipe"]
        playerID = event["playerID"]
        self.serverThread.requestCraft(recipe, playerID)
        pass

    def interactionRequestFromClient(self, event):
        playerID = event["playerID"]
        self.serverThread.interactionRequestFromPlayer(playerID)
        pass

    def setHotbar(self, event):
        stackID = event["stackID"]
        hotbarSlot = event["hotbarSlot"]
        playerID = event["playerID"]
        self.serverThread.setHotbarRequest(playerID, hotbarSlot, stackID)
        pass

    def setActiveSlot(self, event):
        playerID = event["playerID"]
        slot = event["slot"]
        self.serverThread.world.eventBus.event(
            "setActiveSlot", {"playerID": playerID, "slot": slot})
        pass

    def respawnPlayerChannels(self, event):
        playerID = event["playerID"]
        self.serverThread.world.eventBus.event(
            "respawnPlayer", {"playerID": playerID})


