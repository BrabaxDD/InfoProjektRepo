from game.ServerClasses import GameObject
import uuid


class Obstacle(GameObject.GameObject):
    def __init__(self, world, posx, posy, posx2, posy2, entityType):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        super().__init__(world, posx, posy, ID, entityType)
        self.world.eventBus.registerListner(self, "playerPositionUpdate")
        self.world.eventBus.registerListner(self, "zombiePositionUpdate")
        self.entityType = entityType
        self.thickness = 10
        self.posx2 = posx2
        self.posy2 = posy2
        self.lastPlayerPosx = {}
        self.lastPlayerPosy = {}
        self.lastZombiePosx = {}
        self.lastZombiePosy = {}
        self.framecount = 0
        pass

    def deleteSelf(self):
        pass

    def process(self, delta):
        self.framecount += 1
        pass

    def broadcast(self):
        self.world.broadcastPosition(
            self.ID, self.posx, self.posy, self.entityType)
        self.world.broadcastWallInformation(
            self.posx2, self.posy2, self.thickness, self.ID)
        pass

    def event(self, eventString, action):
        if eventString == "zombiePositionUpdate":
            posx = action["posx"]
            posy = action["posy"]
            zombieID = action["zombieID"]
            if zombieID in self.lastZombiePosx and zombieID in self.lastZombiePosy:
                collision = self.do_intersect(
                    (posx, posy),
                    (self.lastZombiePosx[zombieID],
                     self.lastZombiePosy[zombieID]),
                    (self.posx, self.posy), (self.posx2, self.posy2))
                if collision:
                    print(
                        "log: interupted Zombie movement of Player with ID: " + str(zombieID))
                    self.world.eventBus.event("zombieForbiddenMovement",
                                              {"zombieID": zombieID, "lastPosx": self.lastZombiePosx[zombieID], "lastPosy": self.lastZombiePosy[zombieID]})
                else:
                    self.lastZombiePosx[zombieID] = posx
                    self.lastZombiePosy[zombieID] = posy
            else:
                self.lastZombiePosx[zombieID] = posx
                self.lastZombiePosy[zombieID] = posy

            pass

        if eventString == "playerPositionUpdate":
            posx = action["posx"]
            posy = action["posy"]
            playerID = action["ID"]
            if playerID in self.lastPlayerPosx and playerID in self.lastPlayerPosy:
                collision = self.do_intersect(
                    (posx, posy),
                    (self.lastPlayerPosx[playerID],
                     self.lastPlayerPosy[playerID]),
                    (self.posx, self.posy), (self.posx2, self.posy2))
                if collision:
                    print(
                        "log: interupted Player movement of Player with ID: " + str(playerID))
                    self.world.eventBus.event("playerForbiddenMovement",
                                              {"playerID": playerID, "lastPosx": self.lastPlayerPosx[playerID], "lastPosy": self.lastPlayerPosy[playerID]})
                else:
                    self.lastPlayerPosx[playerID] = posx
                    self.lastPlayerPosy[playerID] = posy
            else:
                self.lastPlayerPosx[playerID] = posx
                self.lastPlayerPosy[playerID] = posy

            pass


# Code von CHATGPT

    def do_intersect(self, p1, q1, p2, q2):
        # Hilfsfunktion zur Orientierung
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # kollinear
            return 1 if val > 0 else 2  # 1 = im Uhrzeigersinn, 2 = gegen Uhrzeigersinn

        # Prüfen, ob Punkt `p` auf der Strecke `q-r` liegt
        def on_segment(p, q, r):
            if min(q[0], r[0]) <= p[0] <= max(q[0], r[0]) and min(q[1], r[1]) <= p[1] <= max(q[1], r[1]):
                return True
            return False

        # Orientierung der vier Punkte berechnen
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # Allgemeiner Fall
        if o1 != o2 and o3 != o4:
            return True

        # Sonderfälle
        # p2 liegt auf Segment p1-q1
        if o1 == 0 and on_segment(p2, p1, q1):
            return True
        # q2 liegt auf Segment p1-q1
        if o2 == 0 and on_segment(q2, p1, q1):
            return True
        # p1 liegt auf Segment p2-q2
        if o3 == 0 and on_segment(p1, p2, q2):
            return True
        # q1 liegt auf Segment p2-q2
        if o4 == 0 and on_segment(q1, p2, q2):
            return True

        return False
