import folium
import requests
from tkinter import *
import webbrowser

lat = 50.920652         # Breitengrad vgl Äquator
lon = 6.937008          # Längengrad vgl Greenwich

maplayer = folium.Map(location=[lat, lon],
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

geolayer = folium.FeatureGroup()

geolayer.add_child(folium.GeoJson(open("test.geojson",
                                       ).read()))

geolayer.add_to(maplayer)

maplayer.save('test.html')

window = Tk()
window.title("Kat2S")



def action():
    webbrowser.open('test.html')
    window.destroy()


button = Button(window, text="Hit me!", command=action)
button.pack(side=LEFT)

mainloop()
