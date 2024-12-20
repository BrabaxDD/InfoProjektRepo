from game.ServerClasses import Inventory
from game.ServerClasses import ItemsStack


def asDict(obj):
    if isinstance(obj, Inventory.Inventory):
        return obj.__dict__
    elif isinstance(obj, ItemsStack.ItemStack):
        return obj.__dict__
