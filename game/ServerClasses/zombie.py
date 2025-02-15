from game.ServerClasses import GameObject
import datetime
import uuid
from math import sqrt
import random
from game.ServerClasses import ItemsStack


class Zombie(GameObject.GameObject):
    def __init__(self, world, posx, posy):
        ID = uuid.uuid4().int
        ID = ID % 4001001001
        super().__init__(world, posx, posy, ID=ID, entityType="Zombie")
        self.world.eventBus.registerListner(self, "playerPositionUpdate")
        self.world.eventBus.registerListner(self, "playerHit")
        self.world.eventBus.registerListner(self, "zombieForbiddenMovement")

        self.HP = 200
        self.velocity = 200
        self.timesincelasthit = 0
        self.nearestPlayerID = None
        self.nearestPlayerPosx = None
        self.nearestPlayerPosy = None
        self.nearestPlayerDistance = float("inf")
        self.lastAttackedPlayerID = None  # Keep track of last hit player
        self.playerDistances = {}

    def deleteSelf(self):
        self.world.eventBus.deRegisterListner(self, "playerHit")
        self.world.eventBus.deRegisterListner(self, "playerPositionUpdate")
        self.world.eventBus.deRegisterListner(self, "zombieForbiddenMovement")
        super().deleteSelf()

    def broadcast(self):
        self.world.broadcastPosition(self.ID, self.posx, self.posy, "Zombie")

    def process(self, delta):
        self.timesincelasthit += delta

        # If no near player, don't move
        if self.nearestPlayerDistance >= 1000:
            return
        
        # If a player was attacked recently, keep hitting them
        if self.lastAttackedPlayerID is not None:
            self.nearestPlayerID = self.lastAttackedPlayerID
            self.nearestPlayerDistance = self.playerDistances.get(self.nearestPlayerID, float("inf"))
        
        # Move towards the nearest player
        if self.nearestPlayerID and self.nearestPlayerDistance >= 4:
            dx = self.nearestPlayerPosx - self.posx
            dy = self.nearestPlayerPosy - self.posy
            # Calculate movement based on distance
            movex = (dx / self.nearestPlayerDistance) * self.velocity * delta
            movey = (dy / self.nearestPlayerDistance) * self.velocity * delta
            self.newPositon(self.posx + movex, self.posy + movey)

            # Broadcast the new position after movement
            self.world.eventBus.event("zombiePositionUpdate", {
                "zombieID": self.ID, "posx": self.posx, "posy": self.posy
            })

        # If the player is within attack range, attack the player
        if self.nearestPlayerDistance < 50 and self.timesincelasthit > 1.5:
            self.timesincelasthit = 0
            self.lastAttackedPlayerID = self.nearestPlayerID  # Store last hit player
            self.world.eventBus.event("zombieHit", {
                "PlayerID": self.nearestPlayerID, "Damage": 50, "Zombie": self
            })

    def event(self, eventString, action):
        if eventString == "playerPositionUpdate":
            ID = action["ID"]
            posx = action["posx"]
            posy = action["posy"]
            distance = sqrt((posx - self.posx) ** 2 + (posy - self.posy) ** 2)

            self.playerDistances[ID] = distance

            # Only update target if this player is closer OR it is the last attacked player
            if distance < self.nearestPlayerDistance or ID == self.lastAttackedPlayerID:
                self.nearestPlayerID = ID
                self.nearestPlayerPosx = posx
                self.nearestPlayerPosy = posy
                self.nearestPlayerDistance = distance

        elif eventString == "playerHit":
            player = action["Player"]
            dmg = action["dmg"]
            if (player.posx - self.posx)**2 + (player.posy - self.posy)**2 < 2500:
                self.HP -= dmg
                if self.HP <= 0:
                    player.addItemToInv(ItemsStack.ItemStack("Rags", random.randint(1, 3), uuid.uuid4().int % 4001001001))
                    if random.randint(0, 3) == 0:
                        player.addItemToInv(ItemsStack.ItemStack("Screwdriver", 1, uuid.uuid4().int % 4001001001))
                    self.deleteSelf()

        elif eventString == "zombieForbiddenMovement":
            if self.ID == action["zombieID"]:
                self.posx = action["lastPosx"]
                self.posy = action["lastPosy"]
