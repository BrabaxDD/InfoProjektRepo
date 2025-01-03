from game.ServerClasses import World
from game.ServerClasses import Inventory, ItemsStack
import time
from game.ServerClasses import GameObject
import uuid


class Player(GameObject.GameObject):
    def __init__(self, ID, world: World.World):
        super().__init__(world, 0, 0, ID, "Player")
        self.velocity = 310
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.world.eventBus.registerPlayerActionListner(self)
        self.world.eventBus.registerPlayerGenerateItemListner(self)
        self.world.eventBus.registerPlayerRequestHitListner(self)
        self.world.eventBus.registerZombieHitListner(self)
        self.world.eventBus.registerPlayerForbiddenMovementListner(self)
        self.Inventory = Inventory.Inventory()
        self.lastHit = time.perf_counter()
        self.HP = 200
        self.world.broadcastHealth(self.ID, self.HP, "Player")

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
            if time.perf_counter() - self.lastHit > 0.5:
                self.lastHit = time.perf_counter()
                self.world.eventBus.playerHit(
                    {"ID": self.ID, "Player": self, "direction": action["direction"]})

    def process(self, delta):
        NewPosx = self.posx
        NewPosy = self.posy
        if self.right:
            NewPosx = delta*self.velocity + self.posx
        if self.left:
            NewPosx = delta*self.velocity*(-1) + self.posx
        if self.down:
            NewPosy = delta*self.velocity + self.posy
        if self.up:
            NewPosy = delta*self.velocity*(-1) + self.posy
        self.newPositon(newPosx=NewPosx, newPosy=NewPosy)

    def newPositon(self, newPosx, newPosy):
        self.posx = newPosx
        self.posy = newPosy
        self.world.eventBus.playerPositionUpdate(
            {"posx": self.posx, "posy": self.posy, "ID": self.ID})

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Player")

    def treeHit(self, tree):
        self.Inventory.addItem(ItemsStack.ItemStack(
            "Wood", 3, str(uuid.uuid4())), 0)
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    def zombieHit(self, action):
        if action["PlayerID"] == self.ID:
            self.HP = self.HP - action["Damage"]
            self.world.broadcastHealth(self.ID, self.HP, "Player")

    def playerForbiddenMovement(self, action):
        playerID = action["playerID"]
        if playerID == self.ID:
            print(
                "log: Player got Interupted in Movement, the player ID is: " + str(self.ID))
            print("log: Player got Teleported deltax: " + str(self.posx -
                  action["lastPosx"]) + " deltay: " + str(self.posy - action["lastPosy"]))
            self.newPositon(
                newPosx=action["lastPosx"], newPosy=action["lastPosy"])
