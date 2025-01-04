from dataclasses import dataclass
from game.ServerClasses import jsonSerializer
import json


@dataclass
class Inventory:
    def __init__(self):
        self.items = []

    def addItem(self, itemStack):
        self.items.append(itemStack)

    def removeItem(self, stackID):
        toRemove = None
        indexToRemove = None
        for i,itemStack in enumerate(self.items):
            print(itemStack.stackID)
            print(stackID)
            print(itemStack.stackID == stackID)
            if itemStack.stackID == stackID:
                toRemove = itemStack
                indexToRemove = i
        if indexToRemove is not None:
            print(json.dumps(toRemove, default=jsonSerializer.asDict))
            print(json.dumps(self, default=jsonSerializer.asDict))
            del self.items[indexToRemove]
            print(json.dumps(self, default=jsonSerializer.asDict))
        print(json.dumps(self, default=jsonSerializer.asDict))
