import random


def WavefunctionCollapse(AllowedNeigbours, xsize, ysize, possibilities):
    # Allowed Neighbors ist eine dict das für alle Zahlen von 0 bis n alle erlaubten nachbarn in einer Liste enthält
    # map ist ein 2 dimensionales arrey wo überall ein array drin steht mit erster stelle anzahl der möglichkeiten und an zweiter stelle eine Liste der Möglichkeiten
    collapsed = 0
    map = []
    for i in range(xsize):
        map.append([])
        for j in range(ysize):
            map[i].append([possibilities, list(range(possibilities)), False])
    print(map)
    while collapsed < xsize*ysize:
        min = possibilities
        ymin = 0
        xmin = 0
        for x in range(xsize):
            for y in range(ysize):
                if map[x][y][0] < min and not map[x][y][2]:
                    min = map[x][y][0]
                    xmin = x
                    ymin = y
        print(str(xmin) + " " + str(ymin))
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
        print(map)
    finalmap = []
    for x in range(xsize):
        finalmap.append([])
        for y in range(ysize):
            finalmap[x].append(map[x][y][1][0])
    return finalmap


print(WavefunctionCollapse({0: [1], 1: [0, 2], 2: [1]}, 10, 10, 3))
