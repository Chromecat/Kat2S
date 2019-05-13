import requests
import math
import json
import re

with open('data.config') as json_file:
    data = json.load(json_file)
    lat = float(data["lat"])
    lon = float(data["lon"])
    endtime = int(data["endtime"])


request = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="
                 + str(lat)
                 + "&lon="
                 + str(lon)
                 + "&appid=c30853926307db7c20b1369a94023fca").text

response = json.loads(request)

windspeed = response["wind"]["speed"]
winddirection = response["wind"]["deg"]

# das unter mir alles in eine schleife die eine liste erstellt und immer +1 min

newlat = lat + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) * windspeed * 60
newlon = lon + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) * windspeed * 60

# hier einen string erstellen die die liste in das json format überträgt und dann unter ersetzen 

with open('dummy.geojson') as file:
    data = file.read()
    data = re.sub("XXX", "["+str(lat)+","+str(lon)+"],["+str(newlat)+","+str(newlon)+"]", data)

with open('1.geojson', 'w') as save:
    save.write(data)

