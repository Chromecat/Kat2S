import requests
import math
import json
import re
import folium
import os

if not os.path.exists('html'):
    os.makedirs('html')

with open('data.config') as json_file:
    data = json.load(json_file)
    lat = float(data["lat"])
    lon = float(data["lon"])
    endtime = int(data["endtime"])

maplayer = folium.Map(location=[lat, lon],
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

geolayer = folium.FeatureGroup()

folium.Marker([lat, lon], popup='Point Zero').add_to(maplayer)

request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="
                 + str(lat)
                 + "&lon="
                 + str(lon)
                 + "&appid=c30853926307db7c20b1369a94023fca").text

response = json.loads(request)

windspeed = response["wind"]["speed"]
winddirection = 7 #response["wind"]["deg"]

coord = [[lon, lat]]

for x in range(0, endtime):
    with open('dummy.geojson') as file:
        data = file.read()
        data = re.sub("XXX", str(coord), data)

    with open('temp.geojson', 'w') as save:
        save.write(data)

    geolayer.add_child(folium.GeoJson(open("temp.geojson",
                                           ).read()))

    geolayer.add_to(maplayer)

    maplayer.save('./html/' + str(x) + '.html')
    newlon = coord[x][0] + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) * windspeed * 60
    newlat = coord[x][1] + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) * windspeed * 60
    coord.append([newlon, newlat])







