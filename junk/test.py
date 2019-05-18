import json, folium, re, math

x = {
    "lat": "50.920652",
    "lon": "6.937008",
    "endtime": "10"
}

lat = 50.920652
lon = 6.937008

with open('data.config', 'w') as outfile:
    json.dump(x, outfile)

maplayer = folium.Map(location=[50.920652, 6.937008],
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

coordin = []

for x in range(0, 380, 20):
    newlon = lon + (180 / (math.pi * 6137000)) * math.cos(math.radians(x))\
             / math.cos(lat * math.pi/180) * 10 * 60
    newlat = lat + (180 / (math.pi * 6137000)) * math.sin(math.radians(x))\
             * 10 * 60
    coordin.append([newlon, newlat])


with open('dummyline.geojson') as file:
    data = file.read()
    data = re.sub("XXX", str(coordin), data)

with open('circle.geojson', 'w') as save:
    save.write(data)

geolayer = folium.FeatureGroup()

geolayer.add_child(folium.GeoJson(open("circle.geojson",
                                       ).read()))

geolayer.add_to(maplayer)

maplayer.save('polygoncircle.html')
