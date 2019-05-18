import folium
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import HeatMap
#import requests


lat = 50.920652         # Breitengrad vgl Äquator
lon = 6.937008          # Längengrad vgl Greenwich

#r = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=50.920652&lon=6.937008&appid=c30853926307db7c20b1369a94023fca")


maplayer = folium.Map(location=[lat, lon],
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

geolayer = folium.FeatureGroup()

geolayer.add_child(folium.GeoJson(open("./junk/circle.geojson").read()))

#geolayer.add_child(folium.GeoJson(open("test.geojson",
#                                       ).read()))

geolayer.add_to(maplayer)

maplayer.save('test.html')
