class EventBus:
    def __init__(self):
        self.Listners = {}
        pass


    def registerListner(self, listner, eventString):
        if eventString in self.Listners:
            self.Listners[eventString].append(listner)
        else:
            self.Listners[eventString] = [listner]

    def event(self, eventString, action):
        for listner in self.Listners[eventString]:
            listner.event(eventString, action)

    def deRegisterListner(self, listner, eventString):
        self.Listners[eventString].remove(listner)
