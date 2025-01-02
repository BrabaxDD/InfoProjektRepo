import threading
import time
from game.consumers import gameServer
from game.ServerClasses import World
from game.ServerClasses.Player import Player


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

        while running:
            if not self.gameServerSocket.getRunning():
                running = False
            last = now
            now = time.perf_counter()
            delta = now - last
            self.world.process(delta)
            self.world.broadcast()

    def playerActionUpdate(self, action):
        self.world.eventBus.playerAction(action)

    def login(self, ID):
#        if not self.firstplayer:
        self.world.generate()
#        self.firstplayer = True
        self.world.addGameobject(Player(ID, self.world))

    def broadcastPosition(self, ID, posx, posy, entityType):
        self.gameServerSocket.updatePosition(ID, posx, posy, entityType)

    def playerGenerateItem(self, event):
        self.world.eventBus.playerGenerateItem(event)

    def broadcastPlayerInventoryUpdate(self, ID, Inventory):
        self.gameServerSocket.updateInventory(ID, Inventory)

    def hitRequestFromPlayer(self, ID, direction):
        self.world.eventBus.playerRequestHit(
            {"ID": ID, "direction": direction})

    def broadcastHealthUpdate(self, ID, entityType, HP):
        self.gameServerSocket.updateHealth(ID, entityType, HP)
