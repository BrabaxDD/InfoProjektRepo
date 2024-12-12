class Inventory:
    def __init__(self):
        self.items = []
    def addItem(self,item,index):
        self.items.insert(index,item)
