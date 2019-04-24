import requests
import math

lat = 50.920652         # Breitengrad vgl Äquator in Grad
lon = 6.937008          # Längengrad vgl Greenwich in Grad

r = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="
                 + str(lat)
                 + "&lon="
                 + str(lon)
                 + "&appid=c30853926307db7c20b1369a94023fca")

print(r.text)

winddirection = 130.5     # in Grad
windspeed = 10.2          # in m/s

newlat = lat + (180 / (math.pi * 6137000)) * math.sin(math.radians(winddirection)) * windspeed * 60
# nächster punkt = alter punkt + faktor m -> grad * windrichtung * windgeschwindigkeit für eine minute
newlon = lon + (180 / (math.pi * 6137000)) * math.cos(math.radians(winddirection)) * windspeed * 60
# nächster punkt = alter punkt + faktor m -> grad * windrichtung * windgeschwindigkeit für eine minute


print(newlat)
print(lat)
print()
print(newlon)
print(lon)

# liste erstellen und für jeden punkt ein wert eingeben.
