import requests
import json
import folium
import os
import datetime
import shutil
import functions
import math


def generatehtml():

    if os.path.exists('html'):  # erstellen des subfolders html
        shutil.rmtree('html')

    os.makedirs('html')

    if not os.path.exists('temp'):  # erstellen des subfolder temp
        os.makedirs('temp')

    with open('data.config') as json_file:  # lesen der config datei lat, lon, numbersteps, timesteps
        data = json.load(json_file)
        lat = float(data["lat"])
        lon = float(data["lon"])
        numbersteps = int(data["numbersteps"])
        timesteps = int(data["timesteps"])

    maplayer = folium.Map(location=[lat, lon],  #create map
                      tiles="Stamen Toner",
                      zoom_start=16
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

    try:
        winddirection = response["wind"]["deg"]
    except KeyError:
        winddirection = 0

    print(response)

    # Vorbereitungsende

    coordcorepoint = [[lon, lat]]  # erstellen der liste coordcorepoint
    polygon1 = [[lon, lat]]
    polygon2 = [[lon, lat]]
    polygon3 = [[lon, lat]]
    polygon4 = [[lon, lat]]

    for x in range(0, numbersteps):  # mainloop für minuten bis numbersteps
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

        maplayer.save('./html/' + str(x * timesteps) + '.html')

        functions.newpointcore(coordcorepoint, x, windspeed, winddirection, timesteps)  # neuer core point

        distance = functions.distancepoints(coordcorepoint[0][0], coordcorepoint[0][1], coordcorepoint[1][0], coordcorepoint[1][1])
        yellow = functions.createangle((5 * (math.log1p(5 * (x+1)))), distance)
        red = functions.createangle((50 * (math.log1p(5 * (x+1)))), distance)

        functions.newpointpoly(coordcorepoint, x, windspeed, winddirection, yellow, polygon1, polygon2, timesteps)  # red
        functions.newpointpoly(coordcorepoint, x, windspeed, winddirection, red, polygon3, polygon4, timesteps)  # yellow

    shutil.rmtree('temp')  # remove temp files

    print(coordcorepoint)