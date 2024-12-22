from game.ServerClasses import GameObject
from random import random
import uuid


class Tree(GameObject.GameObject):
    def __init__(self, world):
        ID = uuid.uuid4().int
        super().__init__(world, random()*300, random()*300, ID, "Tree")
        self.world.eventBus.registerPlayerHitListner(self)

    def broadcast(self):
        self.world.broadcastPosition("TestTree", self.posx, self.posy, "Tree")

    def process(self, delta):
        pass

    def playerHit(self, action):
        direction = action["direction"]
        playerID = action["ID"]
        player = action["Player"]
        if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 2500:
            player.treeHit(self)
