import requests, math, json, re, folium, os, datetime, shutil, functions

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
                      zoom_start=17
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

windspeed = 1  # response["wind"]["speed"]
winddirection = 0  # response["wind"]["deg"]

print(response)

coordcorepoint = [[lon, lat]]  # erstellen der liste coordcorepoint
polygon1 = [[lon, lat]]
polygon2 = [[lon, lat]]
polygon3 = [[lon, lat]]
polygon4 = [[lon, lat]]

steps = 1

for x in range(0, endtime):  # mainloop für minuten bis endtime
    functions.creategeojson(coordcorepoint, './geojson/dummyline.geojson')
    functions.creategeojson(polygon1, './geojson/dummypolygonred.geojson')
    functions.creategeojson(polygon2, './geojson/dummypolygonred.geojson')
    functions.creategeojson(polygon3, './geojson/dummypolygonyellow.geojson')
    functions.creategeojson(polygon4, './geojson/dummypolygonyellow.geojson')

    functions.addlayer(polygon3, polygonlayer, maplayer)  # erst 3 und 4 aufgrund der überlagerung
    functions.addlayer(polygon4, polygonlayer, maplayer)
    functions.addlayer(polygon1, polygonlayer, maplayer)
    functions.addlayer(polygon2, polygonlayer, maplayer)
    functions.addlayer(coordcorepoint, corepointlayer, maplayer)

    maplayer.save('./html/' + str(x * steps) + '.html')

    functions.newpointcore(coordcorepoint, x, windspeed, winddirection, steps)  # neuer core point

    distance = functions.distancepoints(coordcorepoint[0][0], coordcorepoint[0][1], coordcorepoint[1][0], coordcorepoint[1][1])
    yellow = functions.createangle(10, distance)   # (0.05 * (math.log1p(5 * (x+1))))
    red = functions.createangle(30, distance)  # 0.5 * (math.log1p(5 * (x+1))))

    functions.newpointpoly(coordcorepoint, x, windspeed, winddirection, yellow, polygon1, polygon2, steps)  # red
    functions.newpointpoly(coordcorepoint, x, windspeed, winddirection, red, polygon3, polygon4, steps)  # yellow

shutil.rmtree('temp')  # remove temp files

print(coordcorepoint)
