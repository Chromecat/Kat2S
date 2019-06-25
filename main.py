import json
from tkinter import *
from selenium import webdriver
import imageio
import os
from myGifGui import opengif
from geopy.geocoders import Nominatim


# lat = 50.920652  # Breitengrad vgl Äquator
# lon = 6.937008  # Längengrad vgl Greenwich


boolean = False

latitude = ""
longitude = ""


def get_lat_lon_of_address():
    geolocator = Nominatim(user_agent="Kat2S")
    address = entryAddress.get()
    location = geolocator.geocode(address)
    print(location.address)
    print(location.latitude, location.longitude)
    locationAddress = location.address
    global latitude
    latitude = location.latitude
    global longitude
    longitude = location.longitude


def create_json_config_file():
    get_lat_lon_of_address()
    content = {
        "lat": latitude,
        "lon": longitude,
        "endtime": 10
    }
    with open('data.config', 'w') as outfile:
        json.dump(content, outfile)


def create_gif():
    if entryAddress.get() and entryMenge.get() and entryBar.get():

        create_json_config_file()
        images = []
        filenames = []
        browser = webdriver.Chrome(executable_path="chromedriver.exe")
        rootpath = os.getcwd() + '/html'
        counter = 0
        numberhtml = 0

        # Number of Files in Dir
        length = len(os.listdir(rootpath))

        while counter < length:
            print('testo')
            browser.get(rootpath + '/' + str(numberhtml) + '.html')
            browser.save_screenshot('screenshots/screenshot' + str(counter) + '.png')
            filenames.append('screenshots/screenshot' + str(counter) + '.png')
            print('Filesname:' + str(len(filenames)))
            counter = counter + 1
            numberhtml = numberhtml + 10

        # browser.get('file:///' + os.getcwd() + '/html/0.html')
        # browser.save_screenshot("screenshots/screenshot0.png")
        # filenames.append('screenshots/screenshot0.png')
        # browser.get('file:///' + os.getcwd() + '/html/10.html')
        # browser.save_screenshot("screenshots/screenshot1.png")
        # filenames.append('screenshots/screenshot1.png')
        # browser.get('file:///' + os.getcwd() + '/html/20.html')
        # browser.save_screenshot("screenshots/screenshot2.png")
        # filenames.append('screenshots/screenshot2.png')
        # browser.get('file:///' + os.getcwd() + '/html/30.html')
        # browser.save_screenshot("screenshots/screenshot3.png")
        # filenames.append('screenshots/screenshot3.png')

        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('animation.gif', images, duration=3)

        browser.close()

        window.destroy()

        try:
            opengif("animation.gif", len(images))
        except:
            print("We know about this exception - GIF-GUI closed")

    else:
        if not boolean:
            show_warning()


# def createmaps():
#     if entryAddress.get() and entryMenge.get() and entryBar.get():
#
#         maplayer = folium.Map(location=[lat, lon],
#                               tiles="Stamen Toner",
#                               zoom_start=15
#                               )
#
#         geolayer = folium.FeatureGroup()
#
#         geolayer.add_child(folium.GeoJson(open("test.geojson",
#                                                ).read()))
#         geolayer.add_to(maplayer)
#
#         maplayer.save('test.html')
#
#         maplayer2 = folium.Map(location=[lat, lon],
#                                tiles="Stamen Toner",
#                                zoom_start=15
#                                )
#
#         geolayer2 = folium.FeatureGroup()
#
#         geolayer2.add_child(folium.GeoJson(open("test2.geojson",
#                                                 ).read()))
#
#         geolayer2.add_to(maplayer2)
#
#         maplayer2.save('test2.html')
#
#         webbrowser.open('test.html')
#         webbrowser.open('test2.html')
#
#         # window.destroy()
#     else:
#         if not boolean:
#             showwarning()


# GUI

window = Tk()
window.title("Kat2S")

row1 = Frame(window)
labelAddress = Label(row1, width=15, anchor='w', text="Adresse*", font=("Helvetica", 13))
entryAddress = Entry(row1)
row1.pack(side=TOP, fill=X, padx=5, pady=5)
labelAddress.pack(side=LEFT)
entryAddress.pack(side=RIGHT, expand=YES, fill=X)

# row1 = Frame(window)
# labelLon = Label(row1, width=15, anchor='w', text="Longitude*", font=("Helvetica", 13))
# entryLon = Entry(row1)
# row1.pack(side=TOP, fill=X, padx=5, pady=5)
# labelLon.pack(side=LEFT)
# entryLon.pack(side=RIGHT, expand=YES, fill=X)

# separator = Frame(height=2, bd=1, relief=SUNKEN)
# separator.pack(fill=X, padx=5, pady=10)
#
# row2 = Frame(window)
# labelLat = Label(row2, width=15, anchor='w', text="Latitude*", font=("Helvetica", 13))
# entryLat = Entry(row2)
# row2.pack(side=TOP, fill=X, padx=5, pady=5)
# labelLat.pack(side=LEFT)
# entryLat.pack(side=RIGHT, expand=YES, fill=X)

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


def show_warning():
    global boolean
    boolean = True
    labelwarning = Label(text="Bitte die mit * gekennzeichneten Felder ausfüllen.", fg="red")
    labelwarning.pack(side=LEFT)


# button = Button(window, text='Create Maps', command=createmaps)
# button.pack(side=LEFT, padx=5, pady=5)

buttonTest = Button(window, text='GenerateGIF', command=create_gif)
buttonTest.pack(side=RIGHT, padx=5, pady=5)

mainloop()
