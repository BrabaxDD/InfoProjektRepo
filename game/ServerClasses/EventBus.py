class EventBus:
    def __init__(self):
        self.playerActionListners = []
        self.playerGenerateItemListners = []
        self.playerRequestHitListners = []
        self.playerHitListners = []
        self.playerPositionUpdateListners = []
        self.zombieHitListners = []
        pass

    def playerAction(self, action):
        for listner in self.playerActionListners:
            listner.playerAction(action)

    def registerPlayerActionListner(self, listner):
        self.playerActionListners.append(listner)

    def playerGenerateItem(self, action):
        for listner in self.playerGenerateItemListners:
            listner.playerGenerateItem(action)

    def registerPlayerGenerateItemListner(self, listner):
        self.playerGenerateItemListners.append(listner)

    def playerRequestHit(self, action):
        for listner in self.playerRequestHitListners:
            listner.playerRequestHit(action)

    def registerPlayerRequestHitListner(self, listner):
        self.playerRequestHitListners.append(listner)

    def playerHit(self, action):
        for listner in self.playerHitListners:
            listner.playerHit(action)

    def registerPlayerHitListner(self, listner):
        self.playerHitListners.append(listner)

    def playerPositionUpdate(self, action):
        for listner in self.playerPositionUpdateListners:
            listner.playerPositionUpdate(action)

    def registerPlayerPositionUpdate(self, listner):
        self.playerPositionUpdate.append(listner)

    def zombieHit(self, action):
        for listner in self.zombieHitListners:
            listner.zombieHit(action)

    def registerZombieHitListner(self, listner):
        self.zombieHitListners.append(listner)
