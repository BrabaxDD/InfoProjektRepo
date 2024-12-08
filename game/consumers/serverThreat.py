import threading
import time
from game.consumers import gameServer
from game.ServerClasses import World
from game.ServerClasses.Player import Player


class serverThreat(threading.Thread):
    def __init__(self, thread_name, thread_ID, gameServerSocket: gameServer):
        threading.Thread.__init__(self)
        self.world = World.World(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.gameServerSocket: gameServer = gameServerSocket
        print("server Worker Threat started")

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
            time.sleep(0.01)
            delta = now - last
            self.world.process(delta)
            self.gameServerSocket.updatePosition()

    def playerActionUpdate(self, action):
        self.world.eventBus.playerAction(action)

    def login(self, ID):
        self.world.objects.append(Player(ID))
    def broadcastPlayerPosition(self,ID,posx,posy):
        self.gameServerSocket.updatePosition(ID,posx,posy)
