from game.ServerClasses import EventBus
from game.ServerClasses import Tree


class World:
    def __init__(self, threat):
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

    def broadcastPosition(self, ID, posx, posy, entityType):
        self.threat.broadcastPosition(ID, posx, posy, entityType)

    def broadcastPlayerInventoryUpdate(self, ID, Inventory):
        self.threat.broadcastPlayerInventoryUpdate(ID, Inventory)

    def addGameobject(self, obj):
        self.objects.append(obj)
        self.threat.gameServerSocket.broadcastNewObject(obj.entityType, obj.ID)
    def generate(self):
        self.addGameobject(Tree.Tree(self))

