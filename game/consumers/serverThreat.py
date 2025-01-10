import threading
import datetime
import time
from game.consumers import gameServer
from game.ServerClasses import World
from game.ServerClasses.Player import Player
from game.ServerClasses import Tree


class serverThreat(threading.Thread):
    def __init__(self, thread_name, thread_ID, gameServerSocket: gameServer):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.gameServerSocket: gameServer = gameServerSocket
        print("server Worker Threat started with ID: " +
              self.gameServerSocket.serverID)

        self.firstplayer = False
        self.world = World.World(self)

    def run(self):
        running = True
        start = time.perf_counter()
        last = None
        now = time.perf_counter()
        self.generated = "False"
        self.world.generate()
        self.generated = "True"
        while running:
            if not self.gameServerSocket.getRunning():
                running = False
            last = now
            now = time.perf_counter()
            delta = now - last
            self.world.process(delta)
            self.world.broadcast()

    def playerActionUpdate(self, action):
        self.world.eventBus.event("playerAction", action)

    def login(self, ID):
        print("log: ein spieler versucht sich auf einem server einzuloggen dessen zustand " +
              self.generated + " ist ")
        if self.generated == "False":
            self.gameServerSocket.respondToLogin(False, ID)
            return
        else:
            self.gameServerSocket.respondToLogin(True, ID)
        self.firstplayer = True
        self.world.addGameobject(Player(ID, self.world))
        self.world.loginNewPlayer(ID)

    def broadcastPosition(self, ID, posx, posy, entityType):
        self.gameServerSocket.updatePosition(ID, posx, posy, entityType)

    def playerGenerateItem(self, event):
        pass

    def broadcastPlayerInventoryUpdate(self, ID, Inventory):
        self.gameServerSocket.updateInventory(ID, Inventory)

    def hitRequestFromPlayer(self, ID, direction):
        self.world.eventBus.event("playerRequestHit",
                                  {"ID": ID, "direction": direction})

    def broadcastHealthUpdate(self, ID, entityType, HP):
        self.gameServerSocket.updateHealth(ID, entityType, HP)

    def broadcastLoginInformation(self, entityID, playerID, entityType):
        self.gameServerSocket.passLoginInformation(
            playerID, entityID=entityID, entityType=entityType)

    def broadcastDeletedGameObject(self, entityType, entityID):
        self.gameServerSocket.broadcastGameObjectDeleted(entityType, entityID)

    def broadcastWallInformation(self, posx2, posy2, thickness, ID):
        self.gameServerSocket.broadcastWallInformation(
            posx2=posx2, posy2=posy2, thickness=thickness, wallID=ID)

    def requestItemStackCombination(self, stackID1, stackID2, playerID):
        self.world.eventBus.event("stackCombinationRequest",
                                  {"stackID1": stackID1, "stackID2": stackID2, "playerID": playerID})
        pass

    def requestCraft(self, recepi, playerID):
        self.world.eventBus.event("playerRequestCraft",
                                  {"recipe": recepi, "playerID": playerID})

    def interactionRequestFromPlayer(self, playerID):
        self.world.eventBus.event("playerRequestInteraction", {
                                  "playerID": playerID})

    def setHotbarRequest(self, playerID, hotbarSlot, stackID):
        self.world.eventBus.event("setHotbarRequest", {
                                  "playerID": playerID, "HotbarSlot": hotbarSlot, "stackID": stackID})
