from dataclasses import dataclass


@dataclass
class ItemStack:
    def __init__(self, ID, size, stackID):
        self.stackID = stackID
        self.size = size
        self.itemID = ID
        self.tags = []
