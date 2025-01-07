from game.ServerClasses import Obstacle
import uuid


class Door(Obstacle.Obstacle):
    def __init__(self, world, posx, posy, posx2, posy2):
        super().__init__(world, posx, posy, posx2, posy2, "Door")
        self.closed = True
        self.world.eventBus.registerListner(self, "playerInteraction")

    def event(self, eventString, action):
        if eventString == "playerPositionUpdate":
            if self.closed:
                super().event(eventString, action)
            else:
                posx = action["posx"]
                posy = action["posy"]
                playerID = action["ID"]
                self.lastPlayerPosx[playerID] = posx
                self.lastPlayerPosy[playerID] = posy
        if eventString == "playerInteraction":
            if self.closed:
                self.closed = False
            else:
                self.closed = True
