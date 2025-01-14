from dataclasses import dataclass
from game.ServerClasses import jsonSerializer
from game.ServerClasses import ItemsStack
import json


@dataclass
class Inventory:
    def __init__(self):
        self.items = []
        self.hotbar = []
        self.hotbarSize = 6
        self.activeSlot = 0
        for i in range(6):
            self.hotbar.append(None)
        self.primaryHand = []

    def addItem(self, itemStack):
        self.items.append(itemStack)

    def removeItem(self, stackID):
        print("log: deleting stack with ID  : " + str(stackID))
        toRemove = None
        indexToRemove = None
        for i, itemStack in enumerate(self.items):
            if int(itemStack.stackID) == int(stackID):
                toRemove = itemStack
                indexToRemove = i
        if indexToRemove is not None:
            del self.items[indexToRemove]
        for i, item in enumerate(self.hotbar):
            if item is not None:
                if item.stackID == stackID:
                    self.hotbar[i] = None
