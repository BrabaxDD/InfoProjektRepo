from game.ServerClasses import Obstacle
import uuid


class Door(Obstacle.Obstacle):
    def __init__(self, world, posx, posy, posx2, posy2):
        super().__init__(world, posx, posy, posx2, posy2, "Door")
        self.closed = True
        self.world.eventBus.registerListner(self, "playerInteraction")
        self.closedPosx2 = posx2
        self.closedPosy2 = posy2
        self.openPosx2 = posx + (posy2 - posy)
        self.openPosy2 = posy + (posx2 - posx)

    def event(self, eventString, action):
        if eventString == "playerPositionUpdate":
            super().event(eventString, action)
        if eventString == "playerInteraction":
            player = action["player"]
            if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 10000:
                if self.closed:
                    self.closed = False
                    self.posx2 = self.openPosx2
                    self.posy2 = self.openPosy2
                else:
                    self.closed = True
                    self.posx2 = self.closedPosx2
                    self.posy2 = self.closedPosy2
                player.setInteractionCooldown(1)
                print("log: the new second coordinates after door  has been interacted with are: " +
                      str(self.posx2) + " " + str(self.posy2))

                self.world.thread.broadcastPosition(
                    self.ID, self.posx, self.posy, self.entityType)
                self.world.thread.broadcastWallInformation(
                    self.posx2, self.posy2, self.thickness, self.ID)

        if eventString == "zombiePositionUpdate":
            super().event(eventString, action)
