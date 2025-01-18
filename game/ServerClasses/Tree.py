from game.ServerClasses import GameObject
from random import random
import uuid
from game.ServerClasses import ItemsStack
import random


class Tree(GameObject.GameObject):
    def __init__(self, world, posx, posy):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        super().__init__(world, posx, posy, ID, "Tree")
        self.world.eventBus.registerListner(self, "playerHit")
        self.world.eventBus.registerListner(self, "playerInteraction")
        self.time = 0
        self.nextUpdate = 0
        self.nextUpdate = random.randint(0, 100) / 100

    def broadcast(self):
        if self.time > self.nextUpdate:
            self.nextUpdate += 1
            self.world.broadcastPosition(self.ID, self.posx, self.posy, "Tree")

    def process(self, delta):
        self.time += delta
        pass

    def event(self, eventString, action):
        if eventString == "playerHit":
            direction = action["direction"]
            playerID = action["ID"]
            player = action["Player"]
            if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 10000:
                player.treeHit(self)
        if eventString == "playerInteraction":
            playerID = action["playerID"]
            player = action["player"]
            if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 10000:
                ID = uuid.uuid4().int
                ID = ID % 4001001001
                player.addItemToInv(ItemsStack.ItemStack("Apple", 1, ID))
                player.setInteractionCooldown(1)
