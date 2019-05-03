import webbrowser

import folium
from tkinter import *


# Map with layer

lat = 50.920652  # Breitengrad vgl Äquator
lon = 6.937008  # Längengrad vgl Greenwich

maplayer = folium.Map(location=[lat, lon],
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

geolayer = folium.FeatureGroup()

geolayer.add_child(folium.GeoJson(open("test.geojson",
                                       ).read()))
geolayer.add_to(maplayer)

maplayer.save('test.html')


# GUIFunctions

# Open map in browser


boolean = False


def createmap():
    if entryLon.get() and entryLat.get() and entryMenge.get() and entryBar.get():
        webbrowser.open('test.html')
        window.destroy()
    else:
        if not boolean:
            showwarning()


# GUI

window = Tk()
window.title("Kat2S")

row1 = Frame(window)
labelLon = Label(row1, width=15, anchor='w', text="Longitude*", font=("Helvetica", 13))
entryLon = Entry(row1)
row1.pack(side=TOP, fill=X, padx=5, pady=5)
labelLon.pack(side=LEFT)
entryLon.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row2 = Frame(window)
labelLat = Label(row2, width=15, anchor='w', text="Latitude*", font=("Helvetica", 13))
entryLat = Entry(row2)
row2.pack(side=TOP, fill=X, padx=5, pady=5)
labelLat.pack(side=LEFT)
entryLat.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row3 = Frame(window)
labelStoff = Label(row3, width=15, anchor='w', text="Stoff*", font=("Helvetica", 13))
choiceValue = StringVar(window)
choices = ['one', 'two', 'three']
choiceValue.set('one')
w = OptionMenu(row3, choiceValue, *choices)
row3.pack(side=TOP, fill=X, padx=5, pady=5)
labelStoff.pack(side=LEFT)
w.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row4 = Frame(window)
labelMenge = Label(row4, width=15, anchor='w', text="Menge*", font=("Helvetica", 13))
entryMenge = Entry(row4)
row4.pack(side=TOP, fill=X, padx=5, pady=5)
labelMenge.pack(side=LEFT)
entryMenge.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row5 = Frame(window)
labelBar = Label(row5, width=15, anchor='w', text="Bar*", font=("Helvetica", 13))
entryBar = Entry(row5)
row5.pack(side=TOP, fill=X, padx=5, pady=5)
labelBar.pack(side=LEFT)
entryBar.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)


def showwarning():
    global boolean
    boolean = True
    labelwarning = Label(text="Bitte die mit * gekennzeichneten Felder ausfüllen.", fg="red")
    labelwarning.pack(side=LEFT)


button = Button(window, text='Create Map', command=createmap)
button.pack(side=LEFT, padx=5, pady=5)

mainloop()
