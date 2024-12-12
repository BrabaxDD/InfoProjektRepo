class EventBus:
    def __init__(self):
        self.playerActionListners = []
        self.playerGenerateItemListners = []
        pass
    def playerAction(self,action):
        for listner in self.playerActionListners:
            listner.playerAction(action)
    def registerPlayerActionListner(self,listner):
        self.playerActionListners.append(listner)
    def playerGenerateItem(self,action):
        for listner in self.playerGenerateItemListners:
            listner.playerGenerateItem(action)
    def registerPlayerGenerateItemListner(self,listner):
        self.playerGenerateItemListners.append(listner)
