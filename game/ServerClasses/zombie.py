from game.ServerClasses import GameObject
import uuid


class Zombie(GameObject.GameObject):
    def __init__(self, world):
        super().__init__(world, posx=0, posy=0, ID=uuid.uuid4(), entityType="Zombie")
        self.nearestPlayerID = 0
        self.nearestPlayerDistance = 10000000000000
        self.velocity = 100
        self.nearestPlayerPosx = 0
        self.nearestPlayerPosy = 0

    def process(self, delta):
        self.posx = ((self.nearestPlayerPosx - self.posx) / self.nearestPlayerDistance * self.velocity) + self.posx
        self.posy = ((self.nearestPlayerPosy - self.posy) / self.nearestPlayerDistance * self.velocity) + self.posy
        pass

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Zombie")

    def playerPositionUpdate(self, action):
        posx = action["posx"]
        posy = action["posy"]
        ID = action["ID"]
        distance = ((posx-self.posx)**2 + (posy + self.posy)**2)**0.5
        if distance < self.nearestPlayerDistance:
            self.nearestPlayerDistance = distance
            self.nearestPlayerID = ID
            self.nearestPlayerPosx = posx
            self.nearestPlayerPosy = posy
