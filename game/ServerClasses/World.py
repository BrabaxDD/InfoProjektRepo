from game.ServerClasses import EventBus
from game.ServerClasses import chest
from game.ServerClasses import Tree
from game.ServerClasses import zombie
from game.ServerClasses import Wall
from game.ServerClasses import Door
import random
import time
import perlin_noise
import queue


class World:
    def __init__(self, threat):
        self.eventBus = EventBus.EventBus()
        self.objects = []
        self.threat = threat
        self.map = None

        pass

    def process(self, delta):
        for gameObject in self.objects:
            gameObject.process(delta)

    def broadcast(self):
        for gameObject in self.objects:
            gameObject.broadcast()

    def broadcastPosition(self, ID, posx, posy, entityType):
        self.threat.broadcastPosition(ID, posx, posy, entityType)

    def broadcastPlayerInventoryUpdate(self, ID, Inventory):
        self.threat.broadcastPlayerInventoryUpdate(ID, Inventory)

    def addGameobject(self, obj):
        self.objects.append(obj)
        self.threat.gameServerSocket.broadcastNewObject(obj.entityType, obj.ID)

    def broadcastHealth(self, ID, HP, entityType):
        self.threat.broadcastHealthUpdate(ID, entityType, HP)
        pass

    # do everything the world needs to do if a new player logs in
    def loginNewPlayer(self, playerID):
        for obj in self.objects:
            if obj.ID != playerID:
                self.threat.broadcastLoginInformation(
                    entityID=obj.ID, entityType=obj.entityType, playerID=playerID)

    def broadcastDeletedGameObject(self, entityType, entityID):
        self.threat.broadcastDeletedGameObject(entityType, entityID)

    def deleteGameObject(self, gameObject):
        self.broadcastDeletedGameObject(gameObject.entityType, gameObject.ID)
        self.objects.remove(gameObject)

    def broadcastWallInformation(self, posx2, posy2, thickness, wallID):
        self.threat.broadcastWallInformation(posx2, posy2, thickness, wallID)
# Ein Tile der Tile Map ist 32 Pixel groß
# Ein Chunk ist 16
# Ein Biom besteht aus mehreren Chunks

    def generate(self):
        self.serverID = self.threat.gameServerSocket.serverID
        sizeX = 32
        sizeY = 32
        self.map = []
        print("log generating Background")
        print("generating Biomes")
        for i in range(sizeX):
            self.map.append([])
            for j in range(sizeY):
                self.map[i].append(0)
#        for tileType in range(1, 3):
#            for i in range(60):
#                length = random.randint(0, 10)
#                radius = random.randint(4, 10)
#                for j in range(length):
#                    xstart = random.randint(0, sizeX)
#                    ystart = random.randint(0, sizeY)
#                    deltax = random.randint(0, 40)
#                    deltax = deltax - 20
#                    deltay = random.randint(0, 40)
#                    deltay = deltay - 20
#                    for z in range(0, 30):
#                        for xt in range(-radius, radius):
#                            for yt in range(-radius, radius):
#                                if yt**2 + xt ** 2 <= radius**2:
#                                    cposx = xstart + int(deltax*z/30) + xt
#                                    cposy = ystart + int(deltay*z/30) + yt
#                                    cposx = cposx % sizeX
#                                    cposy = cposy % sizeY
#
#                                    self.map[cposx][cposy] = tileType


#        noise1 = perlin_noise.PerlinNoise(octaves=3)
#        noise2 = perlin_noise.PerlinNoise(octaves=6)
#        noise3 = perlin_noise.PerlinNoise(octaves=12)
#        noise4 = perlin_noise.PerlinNoise(octaves=24)
#
#        for x in range(sizeX):
#            for y in range(sizeY):
#                noise_val = noise1([x/sizeX, y/sizeY])
#                noise_val += 0.5 * noise2([x/sizeX, y/sizeY])
#                noise_val += 0.25 * noise3([x/sizeX, y/sizeY])
#                noise_val += 0.125 * noise4([x/sizeX, y/sizeY])
#                if noise_val < -0.25:
#                    self.map[x][y] = 1
#
        self.map = WavefunctionCollapse({0: [1, 0], 1: [0, 1, 2], 2: [1, 2, 3], 3: [3,
                                        2]}, xsize=sizeX, ysize=sizeY, possibilities=4)
        print("log: Generating Streets")
#        for tmp in range(6):  # es gibt 6 straßen
#            # die straßen starten am x rand
#            currentx = random.randint(4, sizeX)
#            currenty = 0
#            directionY = True
#            streetWidth = 6  # starßen breite ist 6
#            for i in range(10):  # jede straße besteht aus 10 segmenten
#                if directionY:
#                    # jedes Segment hat die länge 40 bis 200
#                    length = random.randint(0, 5)
#                    length = length * 40
#                    for y in range(length):
#                        for x in range(streetWidth):
#                            self.map[(currentx + x) %
#                                     sizeX][(currenty + y) % sizeY] = 3
#                    currenty += length
#                    directionY = False
#                else:
#                    length = random.randint(0, 5)
#                    length = length * 40
#                    for x in range(length):
#                        for y in range(streetWidth):
#                            self.map[(currentx + x) %
#                                     sizeX][(currenty + y) % sizeY] = 3
#                    currentx += length
#                    directionY = True
        print("log: generating Houses")
        villageposx = 0
        villageposy = 0
        villagesize = 80
#        for i in range(5):
#            self.generateHouse(random.randint(0, villagesize) * 32 + villageposx,
#                               random.randint(0, villagesize) * 32 + villageposy, 128, 128, "North")
#
#        self.generateHouse(64, 256, 128, 128, "north")
        with open("./game/static/images/TileMaps/" + self.serverID + ".txt", "w") as file:
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    # j und i vertausct weil die Tilemap achsengespiegelt gerendert wird
                    file.write(str(self.map[j][i])+",")
                file.write("\n")

        self.addGameobject(Wall.Wall(self, 0, 0, 0, sizeY*32))
        self.addGameobject(Wall.Wall(self, 0, 0, sizeX*32, 0))
        self.addGameobject(Wall.Wall(self, 0, sizeY*32, sizeX*32, sizeY*32))
        self.addGameobject(Wall.Wall(self, sizeX*32, 0, sizeX*32, sizeY*32))

        self.addGameobject(Tree.Tree(self))

        print("log: World Generation Done")

    def generateHouse(self, posx, posy, sizex, sizey, direction):
        self.addGameobject(Wall.Wall(self, posx, posy, posx + sizex, posy))
        self.addGameobject(Wall.Wall(self, posx, posy, posx, posy + sizey))
        self.addGameobject(Wall.Wall(self, posx + sizex,
                           posy, posx + sizex, posy + sizey - 50))
        self.addGameobject(Wall.Wall(self, posx, posy + sizey,
                           posx + sizex, posy + sizey))
        self.addGameobject(Door.Door(self, posx + sizex,
                           posy + sizey - 50, posx + sizex, posy + sizey))
        self.addGameobject(chest.Chest(self, posx, posy))
        for i in range(int(sizex/32)):
            for j in range(int(sizey/32)):
                self.map[int(posx/32) + i][int(posy/32) + j] = 4


def WavefunctionCollapse(AllowedNeigbours, xsize, ysize, possibilities):
    # Allowed Neighbors ist eine dict das für alle Zahlen von 0 bis n alle erlaubten nachbarn in einer Liste enthält
    # map ist ein 2 dimensionales arrey wo überall ein array drin steht mit erster stelle anzahl der möglichkeiten und an zweiter stelle eine Liste der Möglichkeiten
    collapsed = 0
    map = []
    for i in range(xsize):
        map.append([])
        for j in range(ysize):
            map[i].append([possibilities, list(range(possibilities)), False])
    while collapsed < xsize*ysize:
        min = possibilities
        ymin = 0
        xmin = 0
        minmalPossibilities = []
        for x in range(xsize):
            for y in range(ysize):
                if map[x][y][0] <= min and not map[x][y][2]:
                    min = map[x][y][0]
                    xmin = x
                    ymin = y

        for x in range(xsize):
            for y in range(ysize):
                if map[x][y][0] == min and not map[x][y][2]:
                    min = map[x][y][0]
                    minmalPossibilities.append((x, y))
        xmin, ymin = random.choice(minmalPossibilities)
        map[xmin][ymin] = [90000000, [random.choice(map[xmin][ymin][1])], True]
        map[xmin - 1][ymin][1] = list(set(map[xmin - 1][ymin][1])
                                      & set(AllowedNeigbours[map[xmin][ymin][1][0]]))
        map[xmin - 1][ymin][0] = len(map[xmin - 1][ymin][1])
        map[(xmin + 1) % xsize][ymin][1] = list(set(map[(xmin + 1) % xsize][ymin][1])
                                                & set(AllowedNeigbours[map[xmin][ymin][1][0]]))
        map[(xmin + 1) % xsize][ymin][0] = len(map[(xmin + 1) % xsize][ymin][1])
        map[xmin][ymin - 1][1] = list(set(map[xmin][ymin - 1][1])
                                      & set(AllowedNeigbours[map[xmin][ymin][1][0]]))
        map[xmin][ymin - 1][0] = len(map[xmin][ymin - 1][1])
        map[xmin][(ymin + 1) % ysize][1] = list(set(map[xmin][(ymin + 1) % ysize][1])
                                                & set(AllowedNeigbours[map[xmin][ymin][1][0]]))
        map[xmin][(ymin + 1) % ysize][0] = len(map[xmin]
                                               [(ymin + 1) % ysize][1])
        collapsed += 1
    finalmap = []
    for x in range(xsize):
        finalmap.append([])
        for y in range(ysize):
            finalmap[x].append(map[x][y][1][0])
    return finalmap
