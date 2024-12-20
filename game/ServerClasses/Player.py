from game.ServerClasses import World
from game.ServerClasses import Inventory, ItemsStack
import time
from game.ServerClasses import GameObject


class Player(GameObject.GameObject):
    def __init__(self, ID, world: World.World):
        super().__init__(world, 0, 0,ID)
        self.velocity = 290
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.world.eventBus.registerPlayerActionListner(self)
        self.world.eventBus.registerPlayerGenerateItemListner(self)
        self.world.eventBus.registerPlayerRequestHitListner(self)
        self.Inventory = Inventory.Inventory()
        self.lastHit = time.perf_counter()

    def playerAction(self, action):
        if action["ID"] == self.ID:
            self.up = action["up"]
            self.down = action["down"]
            self.right = action["right"]
            self.left = action["left"]
#            print("log: updating Player Actions of Player: " + str(self.ID) + " to " +
#                  str(self.up) + str(self.down) + str(self.right) + str(self.left))

    def playerGenerateItem(self, action):
        print("log: Generating Player Item: " + str(action))        
        if action["ID"] == self.ID:
            self.Inventory.addItem(
                ItemsStack.ItemStack(action["itemID"], 1), 0)
            self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)
            

    def playerRequestHit(self, action):
        if action["ID"] == self.ID:
            if time.perf_counter() - self.lastHit > 1:
                self.lastHit = time.perf_counter()
                self.world.eventBus.playerHit(
                    {"ID": self.ID, "Player": self, "direction": action["direction"]})

    def process(self, delta):
        if self.right:
            self.posx = delta*self.velocity + self.posx
        if self.left:
            self.posx = delta*self.velocity*(-1) + self.posx
        if self.down:
            self.posy = delta*self.velocity + self.posy
        if self.up:
            self.posy = delta*self.velocity*(-1) + self.posy

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Player")

    def treeHit(self, tree):
        self.Inventory.addItem(ItemsStack.ItemStack("Wood", 2), 0)
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)
