import requests, math, json, re, folium, os, datetime, random, shutil, functions

if os.path.exists('html'):  # erstellen des subfolders html
    shutil.rmtree('html')

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
                      zoom_start=140 / endtime  # create function to apply zoom to size of picture
                      )

corepointlayer = folium.FeatureGroup()  # erstellen des corepoint layers
polygonlayer = folium.FeatureGroup()  # erstellen des polygonlayers

folium.Marker([lat, lon], popup='starting point at ' + str(datetime.datetime.now().time())).add_to(maplayer)  # start punkt

request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="  # abfrage über die api
                 + str(lat)
                 + "&lon="
                 + str(lon)
                 + "&appid=c30853926307db7c20b1369a94023fca").text

response = json.loads(request)

windspeed = response["wind"]["speed"]
winddirection = 7 #response["wind"]["deg"]

print(response)

coordcorepoint = [[lon, lat]]  # erstellen der liste coordcorepoint
polygon1 = [[lon, lat]]
polygon2 = [[lon, lat]]
polygon3 = [[lon, lat]]
polygon4 = [[lon, lat]]

steps = 10

for x in range(0, endtime):  # mainloop für minuten bis endtime

    red = functions.createangle(0.05 * (math.log1p(5 * (x+1))))  # hier die ausbreitunsformel für 2000ppm formel - in meter relation auf x(t)
    yellow = functions.createangle(0.5 * (math.log1p(5 * (x+1))))  # hier die ausbreitungsformel für 20ppm s.o.

    functions.creategeojson(coordcorepoint, 'dummyline.geojson')
    functions.creategeojson(polygon1, 'dummypolygonred.geojson')
    functions.creategeojson(polygon2, 'dummypolygonred.geojson')
    functions.creategeojson(polygon3, 'dummypolygonyellow.geojson')
    functions.creategeojson(polygon4, 'dummypolygonyellow.geojson')

    functions.addlayer(polygon3, polygonlayer, maplayer)  # erst 3 und 4 aufgrund der überlagerung
    functions.addlayer(polygon4, polygonlayer, maplayer)
    functions.addlayer(polygon1, polygonlayer, maplayer)
    functions.addlayer(polygon2, polygonlayer, maplayer)
    functions.addlayer(coordcorepoint, corepointlayer, maplayer)

    maplayer.save('./html/' + str(x * steps) + '.html')

    functions.newpointcore(coordcorepoint, x, windspeed, winddirection, steps)  # neuer core point
    functions.newpointpoly(coordcorepoint, x, windspeed, winddirection, red, polygon1, polygon2, steps)  # red
    functions.newpointpoly(coordcorepoint, x, windspeed, winddirection, yellow, polygon3, polygon4, steps)  # yellow

shutil.rmtree('temp')  # remove temp files


# es fehlt berechnung der spreizung durch die addition auf den windrichtungs grad.. und die korrektur der länge um
# rechtwinklig zu bleiben.

# punkt1 durch die ausbreitung berechnen.. verschieben.

