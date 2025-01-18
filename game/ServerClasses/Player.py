from game.ServerClasses import World
import datetime
from game.ServerClasses import Inventory, ItemsStack
import time
from game.ServerClasses import GameObject
import uuid
import json
from game.ServerClasses import jsonSerializer


class Player(GameObject.GameObject):
    def __init__(self, ID, world: World.World):
        super().__init__(world, 1, 1, ID, "Player")
        self.dead = False
        self.velocity = 310
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.world.eventBus.registerListner(self, "playerRequestCraft")
        self.world.eventBus.registerListner(self, "playerAction")
        self.world.eventBus.registerListner(self, "playerRequestHit")
        self.world.eventBus.registerListner(self, "zombieHit")
        self.world.eventBus.registerListner(self, "playerForbiddenMovement")
        self.world.eventBus.registerListner(self, "stackCombinationRequest")
        self.world.eventBus.registerListner(self, "playerRequestInteraction")
        self.world.eventBus.registerListner(self, "setHotbarRequest")
        self.world.eventBus.registerListner(self, "setActiveSlot")
        self.world.eventBus.registerListner(self, "respawnPlayer")
        self.Inventory = Inventory.Inventory()
        self.lastHit = time.perf_counter()
        self.HP = 200
        self.firstBroadcast = False
        self.interactioCooldown = 0
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        self.addItemToInv(ItemsStack.ItemStack("FirstAidKit", 5, ID))
        self.Inventory.hotbar[0] = self.getItemStackByItemID("FirstAidKit")

    def respawn(self):
        self.broadcastRespawn()
        self.newPositon(0, 0)
        self.Inventory = Inventory()
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)
        self.setHealth(300)
        self.dead = False

    def setInteractionCooldown(self, time):
        self.interactioCooldown = time

    def broadcastRespawn(self):
        pass

    def setHealth(self, HP):
        if HP <= 0:
            self.dead = True
            self.world.threat.gameServerSocket.broadcastDeadPlayer(self.ID)
        self.HP = HP
        self.world.broadcastHealth(self.ID, self.HP, "Player")

    def broadcastInit(self):
        self.world.broadcastHealth(self.ID, self.HP, "Player")
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    def process(self, delta):
        if not self.dead:
            self.interactioCooldown -= delta
            if not self.firstBroadcast:
                self.broadcastInit()
            self.firstBroadcast = True
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
        self.world.eventBus.event("objectMove", {
                                  "lastposx": self.posx, "lastposy": self.posy, "posx": newPosx, "posy": newPosy, "gameObject": self})
        self.posx = newPosx
        self.posy = newPosy
        self.world.eventBus.event("playerPositionUpdate",
                                  {"posx": self.posx, "posy": self.posy, "ID": self.ID})

    def broadcast(self):
        if not self.dead:
            self.world.broadcastPosition(
                self.ID, self.posx, self.posy, "Player")

    def treeHit(self, tree):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        self.addItemToInv(ItemsStack.ItemStack("Stick", 3, ID))

    def addItemToInv(self, itemStack):
        self.Inventory.addItem(itemStack)
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    def removeItemFromInv(self, stackID):
        self.Inventory.removeItem(stackID)
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    def changeStackSize(self, stack, newSize):
        stack.size = newSize
        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)

    # später mit einer liste von items und mengen sodass alles gemeinsam abgebrochen wrid
    def consumeMultipleItems(self, itemAmounts):
        for itemAmount in itemAmounts:
            itemID = itemAmount[0]
            neededItemStackSize = itemAmount[1]
            if self.getItemAmountByItemID(itemID) < neededItemStackSize:
                return False
        for itemAmount in itemAmounts:  # zwei listen damit nicht nur die hälfte der items lonsumiert wird und dann abgebrochen
            itemID = itemAmount[0]
            neededItemStackSize = itemAmount[1]
            needed = neededItemStackSize
            while needed > 0:
                stack = self.getItemStackByItemID(itemID)
                if stack.size > needed:
                    self.changeStackSize(stack, stack.size - needed)
                    return True
                elif stack.size == needed:
                    self.removeItemFromInv(stackID=stack.stackID)
                    return True
                elif stack.size < needed:
                    self.removeItemFromInv(stackID=stack.stackID)
                    needed -= stack.size
            print("log: beim Konsumieren von Items von Spieler: " +
                  str(self.ID) + " ist etwas schiefgegangen")
            return False

#    def stackCombinationRequest(self, action):
#        playerID = action["playerID"]
#        if playerID == self.ID:
#            stackID1 = action["stackID1"]
#            stackID2 = action["stackID2"]
#            print("log: trying to combine stackst the ID are: " +
#                  str(stackID1) + " " + str(stackID2))
#            item1 = None
#            item2 = None
#            for itemStack in self.Inventory.items:
#                if itemStack.stackID == stackID1:
#                    item1 = itemStack
#                if itemStack.stackID == stackID2:
#                    item2 = itemStack
#            if (item1 is not None) and (item2 is not None):
#                if item1.itemID == item2.itemID and item1.tags == item2.tags:
#                    ID = uuid.uuid4().int
#                    ID = ID % 4001001001
#                    newItem = ItemsStack.ItemStack(
#                        item1.itemID, item1.size + item2.size, ID)
#                    newItem.tags = item1.tags
#                    print("log: the old items are: ")
#                    print(json.dumps(item1, default=jsonSerializer.asDict))
#                    print(json.dumps(item2, default=jsonSerializer.asDict))
#                    print("log: the new item is: ")
#                    print(json.dumps(newItem, default=jsonSerializer.asDict))
#                    self.removeItemFromInv(str(item1.stackID))
#                    self.removeItemFromInv(str(item2.stackID))
#                    self.addItemToInv(newItem)
#        self.world.broadcastPlayerInventoryUpdate(self.ID, self.Inventory)
#
#    def playerRequestCraft(self, action):
#        playerID = action["playerID"]
#        if playerID == self.ID:
#            recipe = action["recipe"]
#            print("log: player with ID: " + str(self.ID) +
#                  " trys to craft the recipe: " + recipe)
#            match recipe:
#                case "Wood":
#                    print("log: Player with ID: " + str(self.ID) +
#                          " is attempting to craft sticks")
#                    if self.consumeMultipleItems([("Stick", 7)]):
#                        ID = uuid.uuid4().int
#                        ID = ID % 4001001001
#                        self.addItemToInv(
#                            ItemsStack.ItemStack("Wood", 3, ID))

    def getItemAmountByItemID(self, itemID):
        current = 0
        for stack in self.Inventory.items:
            if stack.itemID == itemID:
                current += stack.size
        return current

    def getItemStackByStackID(self, itemID):
        currentStack = None
        for stack in self.Inventory.items:
            if stack.stackID == itemID:
                currentStack = stack
        return currentStack
        pass

    def getItemStackByItemID(self, ItemID):
        currentStack = None
        for stack in self.Inventory.items:
            if stack.itemID == ItemID:
                currentStack = stack
        return currentStack

        pass

    def event(self, eventString, action):
        if eventString == "respawnPlayer":
            if action["playerID"] == self.ID:
                self.respawn()

        if not self.dead:
            if eventString == "setActiveSlot":
                playerID = action["playerID"]
                if playerID == self.ID:
                    slot = action["slot"]
                    self.Inventory.activeSlot = slot
            if eventString == "playerRequestCraft":
                playerID = action["playerID"]
                if playerID == self.ID:
                    recipe = action["recipe"]
                    print("log: player with ID: " + str(self.ID) +
                          " trys to craft the recipe: " + recipe)
                    match recipe:
                        case "Wood":
                            print("log: Player with ID: " + str(self.ID) +
                                  " is attempting to craft sticks")
                            if self.consumeMultipleItems([("Stick", 7)]):
                                ID = uuid.uuid4().int
                                ID = ID % 4001001001
                                self.addItemToInv(
                                    ItemsStack.ItemStack("Wood", 3, ID))
            if eventString == "playerAction":
                if action["ID"] == self.ID:
                    self.up = action["up"]
                    self.down = action["down"]
                    self.right = action["right"]
                    self.left = action["left"]
            if eventString == "setHotbarRequest":
                playerID = action["playerID"]
                if playerID == self.ID:
                    stackID = action["stackID"]
                    hotbarSlot = action["HotbarSlot"]
                    stack = self.getItemStackByStackID(stackID)
                    self.Inventory.hotbar[hotbarSlot] = stack

            if eventString == "playerRequestHit":
                dmg = 50
                if action["ID"] == self.ID:
                    if time.perf_counter() - self.lastHit > 0.5:
                        self.lastHit = time.perf_counter()
                        self.world.eventBus.event("playerHit",
                                                  {"ID": self.ID, "dmg": dmg, "Player": self, "direction": action["direction"]})
            if eventString == "zombieHit":
                if action["PlayerID"] == self.ID:
                    self.setHealth(self.HP - action["Damage"])
                    self.world.broadcastHealth(self.ID, self.HP, "Player")
            if eventString == "playerForbiddenMovement":
                playerID = action["playerID"]
                if playerID == self.ID:
                    print(
                        "log: Player got Interupted in Movement, the player ID is: " + str(self.ID))
                    print("log: Player got Teleported deltax: " + str(self.posx -
                          action["lastPosx"]) + " deltay: " + str(self.posy - action["lastPosy"]))
                    self.newPositon(
                        newPosx=action["lastPosx"], newPosy=action["lastPosy"])
            if eventString == "stackCombinationRequest":
                playerID = action["playerID"]
                if playerID == self.ID:
                    stackID1 = action["stackID1"]
                    stackID2 = action["stackID2"]
                    print("log: trying to combine stackst the ID are: " +
                          str(stackID1) + " " + str(stackID2))
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
                                item1.itemID, item1.size + item2.size, ID)
                            newItem.tags = item1.tags
                            print("log: the old items are: ")
                            print(json.dumps(item1, default=jsonSerializer.asDict))
                            print(json.dumps(item2, default=jsonSerializer.asDict))
                            print("log: the new item is: ")
                            print(json.dumps(
                                newItem, default=jsonSerializer.asDict))
                            self.removeItemFromInv(str(item1.stackID))
                            self.removeItemFromInv(str(item2.stackID))
                            self.addItemToInv(newItem)
                self.world.broadcastPlayerInventoryUpdate(
                    self.ID, self.Inventory)
            if eventString == "playerRequestInteraction":
                if self.interactioCooldown < 0:
                    playerID = action["playerID"]

                    if playerID == self.ID:
                        if self.Inventory.hotbar[self.Inventory.activeSlot] is None:
                            self.world.eventBus.event("playerInteraction",
                                                      {"playerID": self.ID, "player": self})
                            pass
                        else:
                            match self.Inventory.hotbar[self.Inventory.activeSlot].itemID:
                                case "FirstAidKit":
                                    if self.consumeMultipleItems([("FirstAidKit", 1)]):
                                        self.setHealth(self.HP + 1000)
                                        print("log: consumed AIdKit")
