from game.ServerClasses import GameObject
import uuid


class Zombie(GameObject.GameObject):
    def __init__(self, world):
        super().__init__(world, posx=0, posy=0, ID=uuid.uuid4(), entityType="Zombie")

    def process(self, delta):
        pass

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Zombie")
    def playerPositionUpdate(self,action):
        pass

