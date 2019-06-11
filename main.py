import webbrowser

import folium
from tkinter import *
from selenium import webdriver
import imageio
import os

from myGifGui import opengif


# Map with layer

lat = 50.920652  # Breitengrad vgl Äquator
lon = 6.937008  # Längengrad vgl Greenwich

# GUIFunctions

# Open map in browser


boolean = False


def generateimage():
    images = []
    filenames = []
    browser = webdriver.Chrome(executable_path="chromedriver.exe")
    print(os.getcwd())
    browser.get('file:///' + os.getcwd() + './html/0.html')
    browser.save_screenshot("screenshot0.png")
    filenames.append('screenshot0.png')
    browser.get('file:///' + os.getcwd() + './html/1.html')
    browser.save_screenshot("screenshot1.png")
    filenames.append('screenshot1.png')
    browser.get('file:///' + os.getcwd() + './html/2.html')
    browser.save_screenshot("screenshot2.png")
    filenames.append('screenshot2.png')
    browser.get('file:///' + os.getcwd() + './html/3.html')
    browser.save_screenshot("screenshot3.png")
    filenames.append('screenshot3.png')

    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('animation.gif', images, duration=3)

    browser.close()

    window.destroy()

    try:
        opengif("animation.gif", 4)
    except:
        print("We know about this exception - Gif-GUI closed")


def createmaps():
    if entryLon.get() and entryLat.get() and entryMenge.get() and entryBar.get():

        maplayer = folium.Map(location=[lat, lon],
                              tiles="Stamen Toner",
                              zoom_start=15
                              )

        geolayer = folium.FeatureGroup()

        geolayer.add_child(folium.GeoJson(open("test.geojson",
                                               ).read()))
        geolayer.add_to(maplayer)

        maplayer.save('test.html')

        maplayer2 = folium.Map(location=[lat, lon],
                               tiles="Stamen Toner",
                               zoom_start=15
                               )

        geolayer2 = folium.FeatureGroup()

        geolayer2.add_child(folium.GeoJson(open("test2.geojson",
                                                ).read()))

        geolayer2.add_to(maplayer2)

        maplayer2.save('test2.html')

        webbrowser.open('test.html')
        webbrowser.open('test2.html')

        # window.destroy()
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
choices = ['Ammoniak', 'Chlor', 'Isopropylglycolacetat', 'Salzsäure', 'Blausäure']
choiceValue.set('Ammoniak')
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


button = Button(window, text='Create Maps', command=createmaps)
button.pack(side=LEFT, padx=5, pady=5)

buttonTest = Button(window, text='MakeImageAndGIFOfHTML', command=generateimage)
buttonTest.pack(side=RIGHT, padx=5, pady=5)

mainloop()