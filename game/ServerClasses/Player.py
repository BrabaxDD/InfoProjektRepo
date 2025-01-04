from game.ServerClasses import World
from game.ServerClasses import Inventory, ItemsStack
import time
from game.ServerClasses import GameObject
import uuid
import json
from game.ServerClasses import jsonSerializer


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
        self.world.eventBus.registerStackCombinationRequestListner(self)
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
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        self.addItemToInv(ItemsStack.ItemStack("Wood", 3, str(ID)))

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

    def addItemToInv(self, itemStack):
        self.Inventory.addItem(itemStack)
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    def removeItemFromInv(self, stackID):
        self.Inventory.removeItem(stackID)
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    def stackCombinationRequest(self, action):
        playerID = action["playerID"]
        if playerID == self.ID:
            stackID1 = action["stackID1"]
            stackID2 = action["stackID2"]
            print("log: trying to combine stackst the ID are: " + str(stackID1) + " " + str(stackID2))
            item1 = None
            item2 = None
            for itemStack in self.Inventory.items:
                if itemStack.stackID == stackID1:
                    item1 = itemStack
                if itemStack.stackID == stackID2:
                    item2 = itemStack
            if (item1 is not None) and (item2 is not None):
                if item1.itemID == item2.itemID and item1.tags == item2.tags:
                    ID = uuid.uuid4().int
                    ID = ID % 4001001001
                    newItem = ItemsStack.ItemStack(
                        item1.itemID, item1.size + item2.size, str(ID))
                    newItem.tags = item1.tags
                    print("log: the old items are: ")
                    print(json.dumps(item1,default=jsonSerializer.asDict))
                    print(json.dumps(item2,default=jsonSerializer.asDict))
                    print("log: the new item is: ")
                    print(json.dumps(newItem,default=jsonSerializer.asDict))
                    self.removeItemFromInv(str(item1.stackID))
                    self.removeItemFromInv(str(item2.stackID))
                    self.addItemToInv(newItem)
