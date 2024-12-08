from game.ServerClasses import EventBus
from game.consumers import serverThreat


class World:
    def __init__(self, threat: serverThreat.serverThreat):
        self.eventBus = EventBus.EventBus()
        self.objects = []
        self.threat = threat
        pass

    def process(self, delta):
        for gameObject in self.objects:
            gameObject.process(delta)

    def broadcast(self):
        for gameObject in self.objects:
            gameObject.broadcast()

    def broadcastPlayerPosition(self, ID, posx, posy):
        self.threat.broadcastPosition(ID, posx, posy)