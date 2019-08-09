import json
from tkinter import *

from PIL import ImageTk, Image
from selenium import webdriver
import imageio
import os

import producer
from gifGui import opengif
from geopy.geocoders import Nominatim


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


def show_warning():
    global boolean
    boolean = True
    labelwarning = Label(container1, text="Bitte die mit * gekennzeichneten Felder ausfüllen.", fg="red")
    labelwarning.pack(side=LEFT)


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
        producer.generatehtml()
        images = []
        filenames = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--window-size=1920,1080")
        browser = webdriver.Chrome(options=options)
        rootpath = os.getcwd() + '/html'
        counter = 0
        numberhtml = 0

        # Number of Files in Dir
        length = len(os.listdir(rootpath))

        while counter < length:
            browser.get(rootpath + '/' + str(numberhtml) + '.html')
            browser.save_screenshot('screenshots/screenshot' + str(counter) + '.png')
            filenames.append('screenshots/screenshot' + str(counter) + '.png')
            print('Filesname:' + str(len(filenames)))
            counter = counter + 1
            numberhtml = numberhtml + 1

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


# GUI

window = Tk()
window.resizable(width=False, height=False)
window.title("Kat2S")
menubar = Menu(window, bg="#20232A")
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open")
filemenu.add_command(label="Save")
filemenu.add_separator()
filemenu.add_command(label="Exit")
menubar.add_cascade(label="File", menu=filemenu)
# menubar.add_command(label="Test")
window.config(menu=menubar)

container1 = Frame(window)
container1.pack(side=LEFT)

row1 = Frame(container1)
labelAddress = Label(row1, width=15, anchor='w', text="Adresse*", font=("Helvetica", 13))
entryAddress = Entry(row1)
row1.pack(side=TOP, fill=X, padx=5, pady=5)
labelAddress.pack(side=LEFT)
entryAddress.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row2 = Frame(container1)
labelStoff = Label(row2, width=15, anchor='w', text="Stoff*", font=("Helvetica", 13))
choiceValue = StringVar(window)
choices = ['Ammoniak', 'Chlor', 'Isopropylglycolacetat', 'Salzsäure', 'Blausäure']
choiceValue.set('Ammoniak')
w = OptionMenu(row2, choiceValue, *choices)
row2.pack(side=TOP, fill=X, padx=5, pady=5)
labelStoff.pack(side=LEFT)
w.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row3 = Frame(container1)
labelMenge = Label(row3, width=15, anchor='w', text="Menge*", font=("Helvetica", 13))
entryMenge = Entry(row3)
row3.pack(side=TOP, fill=X, padx=5, pady=5)
labelMenge.pack(side=LEFT)
entryMenge.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row4 = Frame(container1)
labelBar = Label(row4, width=15, anchor='w', text="Bar*", font=("Helvetica", 13))
entryBar = Entry(row4)
row4.pack(side=TOP, fill=X, padx=5, pady=5)
labelBar.pack(side=LEFT)
entryBar.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

buttonTest = Button(container1, text='GenerateGIF', command=create_gif)
buttonTest.pack(side=RIGHT, padx=5, pady=5)

container2 = Frame(window)
container2.pack(side=RIGHT, padx=(15, 0))
img = Image.open('rauch.jpg')
newImg = img.resize((180, 260), Image.ANTIALIAS)
newImg = ImageTk.PhotoImage(newImg)
panel = Label(container2, image=newImg)
panel.pack(side=RIGHT)

mainloop()
