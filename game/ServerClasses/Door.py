from game.ServerClasses import Obstacle
import uuid


class Door(Obstacle.Obstacle):
    def __init__(self, world, posx, posy, posx2, posy2):
        super().__init__(world, posx, posy, posx2, posy2,"Door")
        self.closed = True

    def playerPositionUpdate(self, action):
        pass
