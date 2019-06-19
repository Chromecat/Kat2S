import math
import functions


def newpointcore(point, x, windspeed, winddirection, steps):  # erstellen der corelinie
    newlon = point[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) \
             / math.cos(point[x][1] * math.pi / 180) * windspeed * steps * 60
    newlat = point[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) \
             * windspeed * steps * 60
    point.append([newlon, newlat])


def newpointcore1(point, x, windspeed, winddirection, steps):  # erstellen der corelinie
    newlon = point[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) \
             / math.cos(point[x][1] * math.pi / 180) * windspeed * steps * 60
    newlat = point[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) \
             * windspeed * steps * 60
    point.append([newlon, newlat])


functions.lenghtcorrection(6)

point = [[6.937008, 50.920652]]
point1 = [[6.937008, 50.920652]]

for x in range(0, 10):
    newpointcore(point, x, 1, 0, 10)
    newpointcore1(point1, x, 1, 0 + 6, 10)

print(point)
print(point1)

# fehler in der lengenkorrektur ?
