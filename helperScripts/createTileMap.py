import random


x = 100
y = 100
with open("./GameMap.txt", "w") as file:
    for i in range(0, x):
        s = ""
        for j in range(0, y):
            t = str(random.randint(0, 3))
            s += t
            s += ","
        s += "\n"
        file.write(s)
