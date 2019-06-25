import re, folium, math


def creategeojson(point, dummy):  # geojson erstellen aus dummy
    name = str(id(point))
    with open(dummy) as file:  # öffnen des dummy geojson
        data = file.read()
        data = re.sub("XXX", str(point), data)  # ersetzen der XXX durch die coordinaten in die geojson

    with open('./temp/' + name + '.geojson', 'w') as save:  # als eigene geojson speichern
        save.write(data)


def addlayer(point, layer, maplayer):  # erstelltes geojson zur karte hinzufügen
    layer.add_child(folium.GeoJson(open("./temp/" + str(id(point)) + ".geojson",).read()))
    layer.add_to(maplayer)


def newpointcore(point, x, windspeed, winddirection, steps):  # erstellen der corelinie
    newlon = point[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) \
             / math.cos(point[x][1] * math.pi / 180) * windspeed * steps * 60
    newlat = point[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) \
             * windspeed * steps * 60
    point.append([newlon, newlat])


def newpointpoly(point, x, windspeed, winddirection, degreesplit, target1, target2, steps):  # erstellen der polygone
    newpointlon1 = point[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection + degreesplit)) \
             / math.cos(point[x][1] * math.pi/180) * (windspeed * steps * 60) * lenghtcorrection(degreesplit)
    newpointlat1 = point[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection + degreesplit)) \
             * (windspeed * steps * 60) * lenghtcorrection(degreesplit)
    if x >= 1:
        del target1[-1]
    target1.append([newpointlon1, newpointlat1])
    target1.append([point[x+1][0], point[x+1][1]])

    newpointlon2 = point[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection - degreesplit)) \
                  / math.cos(point[x][1] * math.pi / 180) * (windspeed * steps * 60) * lenghtcorrection(degreesplit)
    newpointlat2 = point[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection - degreesplit)) \
                  * (windspeed * steps * 60) * lenghtcorrection(degreesplit)
    if x >= 1:
        del target2[-1]
    target2.append([newpointlon2, newpointlat2])
    target2.append([point[x+1][0], point[x+1][1]])


def createangle(input):
    return math.degrees(math.asin(input/math.sqrt((input * input) + 1)))


def lenghtcorrection(alpha):
    return 1/math.sin(math.radians(90 - alpha))
