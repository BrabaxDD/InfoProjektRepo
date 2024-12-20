from game.ServerClasses import Inventory
from game.ServerClasses import ItemsStack


def asDict(obj):
    if isinstance(obj, Inventory.Inventory):
        return {'items': obj.items}
    elif isinstance(obj, ItemsStack.ItemStack):
        return {'size': obj.size, 'itemID': obj.itemID, 'tags': obj.tags}
