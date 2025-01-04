class EventBus:
    def __init__(self):
        self.playerActionListners = []
        self.playerGenerateItemListners = []
        self.playerRequestHitListners = []
        self.playerHitListners = []
        self.playerPositionUpdateListners = []
        self.zombieHitListners = []
        self.playerForbiddenMovementListners = []
        self.stackCombinationRequesetListners = []
        pass

    def playerForbiddenMovement(self, action):
        for listner in self.playerForbiddenMovementListners:
            listner.playerForbiddenMovement(action)

    def registerPlayerForbiddenMovementListner(self, listner):
        self.playerForbiddenMovementListners.append(listner)

    def deRegisterPlayerForbiddenMovementListner(self, listner):
        self.playerForbiddenMovementListners.remove(listner)

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

    def deRegisterPlayerRequestHitListner(self, listner):
        self.playerRequestHitListners.remove(listner)

    def playerHit(self, action):
        for listner in self.playerHitListners:
            listner.playerHit(action)

    def registerPlayerHitListner(self, listner):
        self.playerHitListners.append(listner)

    def deRegisterPlayerHitListner(self, listner):
        self.playerHitListners.remove(listner)

    def playerPositionUpdate(self, action):
        for listner in self.playerPositionUpdateListners:
            listner.playerPositionUpdate(action)

    def registerPlayerPositionUpdateListner(self, listner):
        self.playerPositionUpdateListners.append(listner)

    def deRegisterPlayerPositionUpdateListner(self, listner):
        self.playerPositionUpdateListners.remove(listner)

    def zombieHit(self, action):
        for listner in self.zombieHitListners:
            listner.zombieHit(action)

    def registerZombieHitListner(self, listner):
        self.zombieHitListners.append(listner)

    def stackCombinationRequest(self, action):
        for listner in self.stackCombinationRequesetListners:
            listner.stackCombinationRequest(action)

    def registerStackCombinationRequestListner(self, listner):
        self.stackCombinationRequesetListners.append(listner)

    def deRegisterStackCombinationRequestListner(self, listner):
        self.stackCombinationRequesetListners.remove(listner)
