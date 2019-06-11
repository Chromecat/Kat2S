import requests, math, json, re, folium, os, datetime, random, shutil

if not os.path.exists('html'):  # erstellen des subfolders html
    os.makedirs('html')

if not os.path.exists('temp'):  # erstellen des subfolder temp
    os.makedirs('temp')

with open('data.config') as json_file:  # lesen der config datei lat, lon, endtime
    data = json.load(json_file)
    lat = float(data["lat"])
    lon = float(data["lon"])
    endtime = int(data["endtime"])

maplayer = folium.Map(location=[lat, lon],  #create map
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

corepointlayer = folium.FeatureGroup()  # erstellen des corepoint layers
polygonlayer1 = folium.FeatureGroup()  # erstellen des polygonlayers

folium.Marker([lat, lon], popup='starting point at ' + str(datetime.datetime.now().time())).add_to(maplayer)  # start punkt

request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="  # abfrage über die api
                 + str(lat)
                 + "&lon="
                 + str(lon)
                 + "&appid=c30853926307db7c20b1369a94023fca").text

response = json.loads(request)

windspeed = response["wind"]["speed"]
winddirection = 7 #response["wind"]["deg"]

coordcorepoint = [[lon, lat]]  # erstellen der liste coordcorepoint
polygon1 = [[lon, lat]]

degreesplit = 20  # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

for x in range(0, endtime):  # mainloop für minuten bis endtime
    with open('dummyline.geojson') as file:  # öffnen des dummy geojson
        data = file.read()
        data = re.sub("XXX", str(coordcorepoint), data)  # ersetzen der XXX durch die coordinaten in die geojson

    with open('./temp/pointtemp.geojson', 'w') as save:
        save.write(data)

    with open('dummypolygon.geojson') as file:  # öffnen des dummy geojson
        data1 = file.read()
        data1 = re.sub("XXX", str(polygon1), data1)  # ersetzen der XXX durch die coordinaten in die geojson

    with open('./temp/poly1temp.geojson', 'w') as save:
            save.write(data1)

    corepointlayer.add_child(folium.GeoJson(open("./temp/pointtemp.geojson",
                                                 ).read()))
    corepointlayer.add_to(maplayer)
    polygonlayer1.add_child(folium.GeoJson(open("./temp/poly1temp.geojson",
                                                ).read()))
    polygonlayer1.add_to(maplayer)

    maplayer.save('./html/' + str(x) + '.html')

    newlon = coordcorepoint[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) \
             / math.cos(lat * math.pi/180) * windspeed * 60
    newlat = coordcorepoint[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) \
             * windspeed * 60
    coordcorepoint.append([newlon, newlat])

    # das der letzte punkt immer bei der anderen liste hinzugefügt wird

    newpointlon = coordcorepoint[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection + degreesplit)) \
             / math.cos(lat * math.pi/180) * (windspeed * 60)  # windspeed * 60 = länge
    newpointlat = coordcorepoint[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection + degreesplit)) \
             * (windspeed * 60)
    polygon1.append([newpointlon, newpointlat])
    degreesplit += (random.random()*20)-10  # random wert durch formel ersetzen

shutil.rmtree('temp')  # remove temp files


# es fehlt berechnung der spreizung durch die addition auf den windrichtungs grad.. und die korrektur der länge um
# rechtwinklig zu bleiben.

# punkt1 durch die ausbreitung berechnen.. verschieben.

