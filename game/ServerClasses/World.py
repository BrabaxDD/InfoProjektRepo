from game.ServerClasses import EventBus
from game.ServerClasses import Tree
from game.ServerClasses import zombie
from game.ServerClasses import Wall
from game.ServerClasses import Door
import time


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
        self.addGameobject(zombie.Zombie(self))
        self.addGameobject(Wall.Wall(self, 100, 0, 100, 300))
        self.addGameobject(Wall.Wall(self, 0, 400, 300, 400))
        self.addGameobject(Door.Door(self,100, 300, 100, 400))

    def broadcastHealth(self, ID, HP, entityType):
        self.threat.broadcastHealthUpdate(ID, entityType, HP)
        pass

    # do everything the world needs to do if a new player logs in
    def loginNewPlayer(self, playerID):
        for obj in self.objects:
            if obj.ID != playerID:
                self.threat.broadcastLoginInformation(
                    entityID=obj.ID, entityType=obj.entityType, playerID=playerID)

    def broadcastDeletedGameObject(self, entityType, entityID):
        self.threat.broadcastDeletedGameObject(entityType, entityID)

    def deleteGameObject(self, gameObject):
        self.broadcastDeletedGameObject(gameObject.entityType, gameObject.ID)
        self.objects.remove(gameObject)

    def broadcastWallInformation(self, posx2, posy2, thickness, wallID):
        self.threat.broadcastWallInformation(posx2, posy2, thickness, wallID)
