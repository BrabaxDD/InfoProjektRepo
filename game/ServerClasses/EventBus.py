class EventBus:
    def __init__(self):
        self.playerActionListners = []
        pass
    def playerAction(self,action):
        for listner in self.playerActionListners:
            listner.playerAction(action)
    def registerPlayerActionListner(self,listner):
        self.playerActionListners.append(listner)

