from dataclasses import dataclass


@dataclass
class ItemStack:
    def __init__(self, itemID, size, stackID):
        self.stackID = stackID
        self.size = size
        self.itemID = itemID
        self.tags = []
