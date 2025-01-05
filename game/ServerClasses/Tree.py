from game.ServerClasses import GameObject
from random import random
import uuid
from game.ServerClasses import ItemsStack


class Tree(GameObject.GameObject):
    def __init__(self, world):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        super().__init__(world, 700, 200, ID, "Tree")
        self.world.eventBus.registerPlayerHitListner(self)
        self.world.eventBus.registerPlayerInteractionListner(self)

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Tree")

    def process(self, delta):
        pass

    def playerHit(self, action):
        direction = action["direction"]
        playerID = action["ID"]
        player = action["Player"]
        if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 10000:
            player.treeHit(self)

    def playerInteraction(self, action):
        playerID = action["playerID"]
        player = action["player"]
        if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 10000:
            ID = uuid.uuid4().int
            ID = ID % 4001001001
            player.addItemToInv(ItemsStack.ItemStack("Apple", 1, ID))
            player.setInteractionCooldown(1)

