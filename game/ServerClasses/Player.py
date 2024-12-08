from game.ServerClasses import World


class Player:
    def __init__(self, ID, world: World.World):
        self.ID = ID
        self.world = world
        self.posx = 0
        self.posy = 0
        self.velocity = 50
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def playerAction(self, action):
        if action["ID"] == self.ID:
            self.up = action["up"]
            self.down = action["down"]
            self.right = action["right"]
            self.left = action["left"]
            pass

    def process(self, delta):
        if self.up:
            self.posx = delta*self.velocity + self.posx
        if self.down:
            self.posx = delta*self.velocity*(-1) + self.posx
        if self.right:
            self.posy = delta*self.velocity + self.posy
        if self.left:
            self.posy = delta*self.velocity*(-1) + self.posy

    def broadcast(self):
        self.world.broadcastPlayerPosition(self.ID, self.posx, self.posy)
