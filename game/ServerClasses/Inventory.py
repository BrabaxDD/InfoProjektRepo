from dataclasses import dataclass
@dataclass
class Inventory:
    def __init__(self):
        self.items = []
    def addItem(self,itemStack,index):
        self.items.insert(index,itemStack)
