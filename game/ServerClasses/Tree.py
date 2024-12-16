from game.ServerClasses import GameObject
from random import random


class Tree(GameObject.GameObject):
    def __init__(self, world):
        super().__init__(world, random()*300, random()*300)

    def broadcast(self):
        self.world.broadcastPosition("TestTree", self.posx, self.posy, "Tree")

    def process(self, delta):
        pass
