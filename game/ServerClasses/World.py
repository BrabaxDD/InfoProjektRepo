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
import math
from multiprocessing.dummy import Pool as ThreatPool
import itertools


class World:
    def __init__(self, threat):
        self.eventBus = EventBus.EventBus()
        self.objects = []
        self.threat = threat
        self.broadCastGameObjectTodo = []
        self.eventBus.registerListner(self, "objectMove")
        self.biomeMap = None
        self.playerChunks = {0: (0, 0)}

        pass

    def process(self, delta):
        def helperPorcess(obj, delta):
            obj.process(delta)

        chunkkoordToIterate = []
        chunkkoordToIterate.append((0, 0))
        for x, y in self.playerChunks.values():
            chunkkoordToIterate.append((x, y))
            chunkkoordToIterate.append(((x-1) % self.chunksx, y))
            chunkkoordToIterate.append(((x+1) % self.chunksx, y))
            chunkkoordToIterate.append((x, (y+1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x-1) % self.chunksx, (y+1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x+1) % self.chunksx, (y+1) % self.chunksy))
            chunkkoordToIterate.append((x, (y-1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x-1) % self.chunksx, (y-1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x+1) % self.chunksx, (y-1) % self.chunksy))
        chunkkoordToIterate = list(set(chunkkoordToIterate))
        objectsToProcess = []
        for chunkCoord in chunkkoordToIterate:
            chunk = self.chunks[chunkCoord]
            objectsToProcess = objectsToProcess + chunk

        pool = ThreatPool(8)
        results = pool.starmap(helperPorcess, zip(
            objectsToProcess, itertools.repeat(delta)))

#            for gameObject in chunk:
#                helperPorcess(gameObject, delta)

    def broadcast(self):
        def helperBroadcast(obj):
            obj.broadcast()
        chunkkoordToIterate = []
        chunkkoordToIterate.append((0, 0))
        for x, y in self.playerChunks.values():
            chunkkoordToIterate.append((x, y))
            chunkkoordToIterate.append(((x-1) % self.chunksx, y))
            chunkkoordToIterate.append(((x+1) % self.chunksx, y))
            chunkkoordToIterate.append((x, (y+1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x-1) % self.chunksx, (y+1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x+1) % self.chunksx, (y+1) % self.chunksy))
            chunkkoordToIterate.append((x, (y-1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x-1) % self.chunksx, (y-1) % self.chunksy))
            chunkkoordToIterate.append(
                ((x+1) % self.chunksx, (y-1) % self.chunksy))
        chunkkoordToIterate = list(set(chunkkoordToIterate))
        objectsToBroadcast = []
        for chunkCoord in chunkkoordToIterate:
            chunk = self.chunks[chunkCoord]
            objectsToBroadcast = objectsToBroadcast + chunk
        pool = ThreatPool(8)
        results = pool.map(helperBroadcast, objectsToBroadcast)
#            for gameObject in chunk:
#                gameObject.broadcast()

    def initialBroadcast(self):
        for obj in self.broadCastGameObjectTodo:
            self.threat.gameServerSocket.broadcastNewObject(
                obj.entityType, obj.ID)

    def broadcastPosition(self, ID, posx, posy, entityType):
        self.threat.broadcastPosition(ID, posx, posy, entityType)

    def broadcastPlayerInventoryUpdate(self, ID, Inventory):
        self.threat.broadcastPlayerInventoryUpdate(ID, Inventory)

    def addGameobject(self, obj):
        self.objects.append(obj)
        if self.threat.generated:
            self.threat.gameServerSocket.broadcastNewObject(
                obj.entityType, obj.ID)
        else:
            self.broadCastGameObjectTodo.append(obj)
        self.chunks[(int(obj.posx/1024), int(obj.posy/1024))].append(obj)

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
# Ein Chunk ist 32
# Ein Biom besteht aus mehreren Chunks

    def generate(self):
        self.serverID = self.threat.gameServerSocket.serverID
        sizeX = 32
        sizeY = 32
        chunksize = 32
        self.chunksx = sizeX/chunksize
        self.chunksy = sizeY/chunksize
        self.map = []
        self.biomeMap = []
        self.chunks = {}
        for x in range(int(self.chunksx)):
            for y in range(int(self.chunksy)):
                self.chunks[(x, y)] = []
        print("log generating Background")
        print("generating Biomes")
        # Biomes 0: Lake 1: Beach 2: Flatland 3: Woods 5: Villages 4: Mountain (not Implemented yet)
#        self.biomes = WavefunctionCollapse({0: [1, 0], 1: [0, 1, 2], 2: [1, 2, 3, 4], 3:
#                                            [3, 2], 4: [2, 4]}, int(sizeX/chunksize), int(sizeY/chunksize),
#                                           possibilities=5)
        height = perlin_noise.PerlinNoise(octaves=1)
        vegetation = perlin_noise.PerlinNoise(octaves=1)
        for i in range(sizeX):
            self.biomeMap.append([])
            for j in range(sizeY):
                self.biomeMap[i].append(1)
        for i in range(sizeX):
            self.map.append([])
            for j in range(sizeY):
                self.map[i].append(1)

        for x in range(sizeX):
            for y in range(sizeY):
                if height([x/sizeX, y/sizeY]) <= -0.2:
                    self.biomeMap[x][y] = 0
                elif height([x/sizeX, y/sizeY]) <= -0.18:
                    self.biomeMap[x][y] = 1
                else:
                    if vegetation([x/sizeX, y/sizeY]) > 0.1:
                        self.biomeMap[x][y] = 2
                    elif vegetation([x/sizeX, y/sizeY]) > 0:
                        self.biomeMap[x][y] = 5
                    else:
                        self.biomeMap[x][y] = 3
#        for bx, biomeColumn in enumerate(self.biomes):
#            for by, biome in enumerate(biomeColumn):
#                pass
# if biome == 0:
#                    A = 2
#                    if by != 0:
#                        for x in range(chunksize):
#                            A1 = random.random() * A
#                            A2 = random.random() * A
#                            for y in range(int(A1 + 0.5*A2 - A1*math.cos(math.pi * (x/chunksize)) - A2*0.5*math.cos(math.pi * 2 * (x/chunksize)))):
#                                self.biomeMap[bx * chunksize +
#                                         x][by*chunksize + y] = 0
#
#
##
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
#                                    self.biomeMap[cposx][cposy] = tileType


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
#                    self.biomeMap[x][y] = 1
#
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
#                            self.biomeMap[(currentx + x) %
#                                     sizeX][(currenty + y) % sizeY] = 3
#                    currenty += length
#                    directionY = False
#                else:
#                    length = random.randint(0, 5)
#                    length = length * 40
#                    for x in range(length):
#                        for y in range(streetWidth):
#                            self.biomeMap[(currentx + x) %
#                                     sizeX][(currenty + y) % sizeY] = 3
#                    currentx += length
#                    directionY = True
        print("log: decorating")
        for x in range(sizeX):
            for y in range(sizeY):
                biome = self.biomeMap[x][y]
                if biome == 0:
                    self.map[x][y] = 0
                if biome == 1:
                    self.map[x][y] = 1
                if biome == 2:
                    self.map[x][y] = 2
                    if random.random() < 0.03:
                        self.addGameobject(Tree.Tree(self, x*32, y*32))
# Häuser werden so generiert das in jedem 16 * 16 abschnitt sich maximal eines befindet
                if biome == 3:
                    self.map[x][y] = 3
                    self.map[x][y] = 6  # set everything to CityGrass
                    if x % 32 == 0 or x % 32 == 1 or x % 32 == 31 or x % 32 == 30:
                        self.map[x][y] = 3

                    if y % 32 == 0 or y % 32 == 1 or y % 32 == 31 or y % 32 == 30:
                        self.map[x][y] = 3
                if biome == 4:
                    self.map[x][y] = 4
                if biome == 5:
                    self.map[x][y] = 5
        for x in range(sizeX):
            for y in range(sizeY):
                biome = self.biomeMap[x][y]
                if biome == 3:
                    if y % 16 == 8 and x % 16 == 8:
                        self.generateHouse(x*32, y*32, 128, 128, "north")


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
        self.addGameobject(
            Wall.Wall(self, 0, sizeY*32 - 1, sizeX*32, sizeY*32))
        self.addGameobject(
            Wall.Wall(self, sizeX*32 - 1, 0, sizeX*32, sizeY*32))

        print("log: World Generation Done")

    def generateHouse(self, posx, posy, sizex, sizey, direction):
        # doorstart ist die menge an pixeln die man gegen den uhrzeigersinn von oben links entgang gehen muss biss die Tür beginnt
        def generateRectWithDoor(posx, posy, sizex, sizey, doorStart, doorEnd):
            if doorStart < sizex:  # door on the northern side
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx + doorStart, posy))
                self.addGameobject(
                    Door.Door(self, posx + doorStart, posy, posx + doorEnd, posy))
                self.addGameobject(
                    Wall.Wall(self, posx + doorEnd, posy, posx + sizex, posy))
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx + sizex, posy, posx + sizex, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx, posy + sizey, posx + sizex, posy + sizey))
                pass
            elif doorStart < sizex + sizey:  # door on the western side
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx + sizex, posy))
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx + sizex, posy, posx + sizex, posy + (doorStart - sizex)))
                self.addGameobject(Door.Door(
                    self, posx + sizex, posy + doorStart - sizex, posx + sizex, posy + doorEnd - sizex))
                self.addGameobject(
                    Wall.Wall(self, posx + sizex, posy + doorEnd - sizex, posx + sizex, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx, posy + sizey, posx + sizex, posy + sizey))
            elif doorStart < sizex * 2 + sizey:  # door on the southern
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx + sizex, posy))
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx + sizex, posy, posx + sizex, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx, posy + sizey, posx + sizex - (doorEnd - sizex - sizey), posy + sizey))
                self.addGameobject(
                    Door.Door(self, posx + sizex - (doorEnd - sizex - sizey), posy + sizey, posx + sizex - (doorStart - sizex - sizey), posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx + sizex - (doorStart - sizex - sizey), posy + sizey, posx + sizex, posy + sizey))
            else:  # door on the eastern side
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx + sizex, posy))
                self.addGameobject(
                    Wall.Wall(self, posx, posy, posx, posy + sizey - (doorEnd - sizex * 2 - sizey)))
                self.addGameobject(Door.Door(self, posx, posy + sizey - (doorEnd - 2 *
                                   sizex - sizey), posx, posy + sizey - (doorStart - sizex * 2 - sizey)))
                self.addGameobject(Wall.Wall(
                    self, posx, posy + sizey - (doorStart - sizex * 2 - sizey), posx, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx + sizex, posy, posx + sizex, posy + sizey))
                self.addGameobject(
                    Wall.Wall(self, posx, posy + sizey, posx + sizex, posy + sizey))

        class Roomtree:
            def __init__(self, type, Child1, Child2, parentDirection, weight, parent):
                self.type = type
                self.Child1 = Child1
                self.Child2 = Child2
                self.parentDirection = parentDirection
                self.weight = weight
                self.parent = parent

            def buildTree(self):
                if self.type == "livingRoom":
                    if random.random() > 0.1:
                        self.Child1 = Roomtree(
                            "corridor", None, None, None, 1, self)
                    if random.random() > 0.1:
                        self.Child2 = Roomtree(
                            "bath", None, None, None, 1, self)

                if self.Child1 is not None:
                    self.Child1.buildTree()
                if self.Child2 is not None:
                    self.Child2.buildTree()

        def partition(room: Roomtree, posx, posy, sizex, sizey):
            verticalSplit = True
            if room.parentDirection == "north":
                verticalSplit = False
                generateRectWithDoor(
                    posx, posy, sizex, sizey, sizex/2 - 16, sizex/2 + 16)
            if room.parentDirection == "east":
                generateRectWithDoor(
                    posx, posy, sizex, sizey, sizey/2 - 16 + sizex, sizey/2 + 16 + sizex)
            if room.parentDirection == "south":
                verticalSplit = False
                generateRectWithDoor(
                    posx, posy, sizex, sizey, sizex/2 - 16 + sizex + sizey, sizex/2 + 16 + sizey + sizex)
            if room.parentDirection == "west":
                generateRectWithDoor(
                    posx, posy, sizex, sizey, sizey/2 - 16 + sizex * 2 + sizey, sizey/2 + 16 + sizex * 2 + sizey)
            if room.Child1 is not None:
                if verticalSplit:
                    room.Child1.parentDirection = "north"
                    partition(room.Child1, posx, posy +
                              0.75 * sizey + sizey * 0.25 * math.tanh(room.weight - room.Child1.weight), sizex, sizey * (1 - 0.75 - 0.25 * math.tanh(room.weight - room.Child1.weight)))
                else:
                    room.Child1.parentDirection = "west"
                    partition(room.Child1, posx +
                              sizex * (0.75 + 0.25 * math.tanh(room.weight - room.Child1.weight)), posy, sizex * (1 - 0.75 - 0.25 * math.tanh(room.weight - room.Child1.weigth)), sizey)
            if room.Child2 is not None:
                if verticalSplit:
                    room.Child2.parentDirection = "south"
                    partition(room.Child2, posx, posy, sizex, sizey * (1 -
                              0.75 - 0.25 * math.tanh(room.weight - room.Child1.weight)))
                else:
                    room.Child2.parentDirection = "east"
                    partition(room.Child2, posx, posy, 1 - 0.75 - 0.25 *
                              math.tanh(room.weight - room.Child1.weigth), sizey)

        tilesizey = int(sizey/32)
        tilesizex = int(sizex/32)
        rooms = Roomtree("livingRoom", None, None, "west", 0, self)
        rooms.buildTree()
        # generate the Room Map
        partition(rooms, posx, posy, sizex, sizey)

#        self.addGameobject(Wall.Wall(self, posx, posy, posx + sizex, posy))
#        self.addGameobject(Wall.Wall(self, posx, posy, posx, posy + sizey))
#        self.addGameobject(Wall.Wall(self, posx + sizex,
#                           posy, posx + sizex, posy + sizey - 50))
#        self.addGameobject(Wall.Wall(self, posx, posy + sizey,
#                           posx + sizex, posy + sizey))
#        self.addGameobject(Door.Door(self, posx + sizex,
#                           posy + sizey - 50, posx + sizex, posy + sizey))
#        self.addGameobject(chest.Chest(self, posx, posy))
#        for i in range(int(sizex/32)):
#            for j in range(int(sizey/32)):
#                self.map[int(posx/32) + i][int(posy/32) + j] = 4

    def event(self, eventString, eventObject):
        if eventString == "objectMove":
            lastposx = eventObject["lastposx"]
            lastposy = eventObject["lastposy"]
            posx = eventObject["posx"]
            posy = eventObject["posy"]
            gameObject = eventObject["gameObject"]
            self.chunks[(int(lastposx/1024), int(lastposy/1024))
                        ].remove(eventObject["gameObject"])
            self.chunks[(int(posx/1024), int(posy/1024))
                        ].append(eventObject["gameObject"])
            if gameObject.entityType == "Player":
                self.playerChunks[gameObject.ID] = (
                    int(gameObject.posx/1024), int(gameObject.posy/1024))


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
