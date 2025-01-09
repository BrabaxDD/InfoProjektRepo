class GameObject:
    def __init__(self,world, posx, posy,ID,entityType):
        self.world = world
        self.posx = posx
        self.posy = posy
        self.ID = ID
        self.entityType = entityType


    def process(self,delta):
        pass
    def broadcast(self):
        self.world.broadcastPosition(self.ID,self.posx,self.posy,self.entityType)
        pass
    def deleteSelf(self):
        self.world.deleteGameObject(self)
