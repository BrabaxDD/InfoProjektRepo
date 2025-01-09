from game.ServerClasses import GameObject
import datetime
import uuid
from math import sqrt
import math
from game.ServerClasses import ItemsStack
import random


class Zombie(GameObject.GameObject):
    def __init__(self, world):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        super().__init__(world, posx=0, posy=0, ID=ID, entityType="Zombie")
        self.world.eventBus.registerListner(self, "playerPositionUpdate")
        self.world.eventBus.registerListner(self, "playerHit")
        self.HP = 200
        self.nearestPlayerID = 0
        self.nearestPlayerDistance = 10000000000000
        self.velocity = 200
        self.nearestPlayerPosx = 1
        self.nearestPlayerPosy = 0
        self.timesincelasthit = 0
        self.playerDistances = {}

    def deleteSelf(self):
        self.world.eventBus.deRegisterListner(self, "playerHit")
        self.world.eventBus.deRegisterListner(self,"playerPositionUpdate")
        super().deleteSelf()

    def process(self, delta):
        self.timesincelasthit += delta
        if self.nearestPlayerDistance < 4:
            pass
        else:
            self.posx += delta * ((self.nearestPlayerPosx - self.posx) /
                                  self.nearestPlayerDistance * self.velocity)
            self.posy += delta * ((self.nearestPlayerPosy - self.posy) /
                                  self.nearestPlayerDistance * self.velocity)
        if self.nearestPlayerDistance < 400 and self.timesincelasthit > 1:
            self.timesincelasthit = 0
            self.world.eventBus.event("zombieHit",
                                      {"PlayerID": self.nearestPlayerID, "Damage": 50, "Zombie": self})
            pass

        self.nearestPlayerDistance = 100000000000000
        self.nearestPlayerPosy = 0
        self.nearestPlayerPosx = 0

        pass

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Zombie")

    def event(self, eventString, action):
        if eventString == "playerHit":
            direction = action["direction"]
            playerID = action["ID"]
            player = action["Player"]
            dmg = action["dmg"]
            if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 2500:
                self.HP -= dmg
            if self.HP < 0:
                ID = uuid.uuid4().int
                ID = ID % 4001001001
                player.addItemToInv(ItemsStack.ItemStack(
                    "Rags", random.randint(1, 3), ID))
                ID = uuid.uuid4().int
                ID = ID % 4001001001
                if random.randint(0, 3) == 0:
                    ID = uuid.uuid4().int
                    ID = ID % 4001001001
                    player.addItemToInv(
                        ItemsStack.ItemStack("Screwdriver", 1, ID))
                self.deleteSelf()
                pass
        if eventString == "playerPositionUpdate":
            posx = action["posx"]
            posy = action["posy"]
            ID = action["ID"]
            distance = sqrt((posx - self.posx)**2 + (posy - self.posy)**2)
            self.playerDistances[ID] = distance
            for key in self.playerDistances:
                dist = self.playerDistances[key]
                if dist < self.nearestPlayerDistance:
                    self.nearestPlayerDistance = distance
                    self.nearestPlayerID = ID
                    self.nearestPlayerPosx = posx
                    self.nearestPlayerPosy = posy
