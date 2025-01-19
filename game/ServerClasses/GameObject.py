import random


class GameObject:
    def __init__(self, world, posx, posy, ID, entityType):
        self.world = world
        self.posx = posx
        self.posy = posy
        self.ID = ID
        self.entityType = entityType
        self.isStatic = False
        self.time = 0
        self.nextUpdate = 0
        self.nextUpdate = random.randint(0, 100) / 100

    def process(self, delta):
        self.time += delta
        pass

    def broadcast(self):
        if self.isStatic:
            if self.time > self.nextUpdate:
                self.nextUpdate += 10
                self.world.broadcastPosition(
                    self.ID, self.posx, self.posy, self.entityType)
        else:
            self.world.broadcastPosition(
                self.ID, self.posx, self.posy, self.entityType)
        pass

    def deleteSelf(self):
        self.world.deleteGameObject(self)

    def newPositon(self, newPosx, newPosy):
        self.world.eventBus.event("objectMove", {
                                  "lastposx": self.posx, "lastposy": self.posy, "posx": newPosx, "posy": newPosy, "gameObject": self})
        self.posx = newPosx
        self.posy = newPosy
