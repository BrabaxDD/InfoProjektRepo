from game.ServerClasses import GameObject
from game.ServerClasses import ItemsStack
import random
import uuid


class Chest(GameObject.GameObject):
    def __init__(self, world, posx, posy):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        super().__init__(world=world, posx=posx, posy=posy, ID=ID, entityType="Chest")
        self.world.eventBus.registerListner(self, "playerInteraction")
        self.content = []
        self.possibleItems = {0: "Apple",
                              1: "Wood", 2: "FirstAidKit", 3: "Scrap"}
        self.generateContent()
        self.looted = False
        self.isStatic = True

    def generateContent(self):
        for i in range(5):
            itemID = random.randint(0, 3)
            itemID = self.possibleItems[itemID]
            ID = uuid.uuid4().int
            ID = ID % 4001001001
            self.content.append(ItemsStack.ItemStack(
                itemID, random.randint(1, 3), ID))

    def event(self, eventString, action):
        if eventString == "playerInteraction":
            player = action["player"]
            if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 10000:
                if not self.looted:
                    self.looted = True
                    for item in self.content:
                        player.addItemToInv(item)
