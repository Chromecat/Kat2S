import json
from tkinter import *
import tkinter.font as font

from PIL import ImageTk, Image
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
import imageio
import os
import shutil

import producer
from file_gui import openfilegui
from gif_gui import opengif
from geopy.geocoders import Nominatim


boolean = False

latitude = ""
longitude = ""
materialChoice = ""
mol = ""
numbersteps = ""
timesteps = ""


def get_lat_lon_of_address():
    geolocator = Nominatim(user_agent="Kat2S")
    address = entryAddress.get()
    location = geolocator.geocode(address)
    print(location.address)
    print(location.latitude, location.longitude)
    global latitude
    latitude = location.latitude
    global longitude
    longitude = location.longitude


def show_warning():
    global boolean
    boolean = True
    labelwarning = Label(container1, text="Bitte die mit * gekennzeichneten Felder entsprechend ausfüllen.", fg="red")
    labelwarning.pack(side=LEFT)


def create_json_config_file():
    get_lat_lon_of_address()
    set_textfield_inputs()

    if materialChoice == "Ammoniak":
        global mol
        mol = 17.031
    elif materialChoice == "Chlor":
        mol = 35.453

    content = {
        "lat": latitude,
        "lon": longitude,
        "materialChoice": materialChoice,
        "mol": mol,
        "numbersteps": numbersteps,
        "timesteps": timesteps
    }

    with open('data.config', 'w') as outfile:
        json.dump(content, outfile)


def set_textfield_inputs():
    global materialChoice
    global timesteps
    global numbersteps
    materialChoice = choiceValue.get()
    timesteps = entryTimesteps.get()
    numbersteps = entryNumbersteps.get()


def create():
    if entryAddress.get() and int(entryTimesteps.get()) and int(entryNumbersteps.get()):

        create_json_config_file()
        window.destroy()
        producer.generatehtml()
        checkforscreenshotsdir()
        images = []
        filenames = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--window-size=1300,680")
        browser = webdriver.Chrome(options=options)
        rootpath = os.getcwd() + '/html'
        counter = 0
        numberhtml = 0

        # Number of Files in Dir
        length = len(os.listdir(rootpath))

        while counter < length:
            browser.get(rootpath + '/' + str(numberhtml) + '.html')
            browser.save_screenshot('screenshots/screenshot' + str(numberhtml) + '.png')
            addtimestamp('screenshots/screenshot' + str(numberhtml) + '.png', numberhtml)
            filenames.append('screenshots/screenshot' + str(numberhtml) + '.png')
            print('Filesname:' + str(len(filenames)))
            counter = counter + 1
            numberhtml = numberhtml + int(timesteps)

        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('animation.gif', images, duration=3)

        openfilegui(len(images))

    else:
        if not boolean:
            show_warning()


def addtimestamp(name, time):

    time = time

    image = Image.open(name)

    draw = ImageDraw.Draw(image)

    fontstyle = ImageFont.truetype('arial.ttf', size=45)

    (x, y) = (100, 50)
    message = str(time) + ' min'
    color = 'rgb(255, 0, 0)'
    draw.text((x, y), message, fill=color, font=fontstyle)
    image.save(name)


def checkforscreenshotsdir():
    if os.path.exists('screenshots'):
        shutil.rmtree('screenshots')
    if not os.path.exists('screenshots'):
        os.mkdir('screenshots')


# GUI

window = Tk()
window.resizable(width=False, height=False)
window.title("Kat2S")

container1 = Frame(window)
container1.pack(side=LEFT)

row1 = Frame(container1)
labelAddress = Label(row1, width=20, anchor='w', text="Adresse*", font=("Helvetica", 13))
entryAddress = Entry(row1)
row1.pack(side=TOP, fill=X, padx=5, pady=5)
labelAddress.pack(side=LEFT)
entryAddress.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row2 = Frame(container1)
labelStoff = Label(row2, width=20, anchor='w', text="Stoff*", font=("Helvetica", 13))
choiceValue = StringVar(window)
choices = ['Ammoniak', 'Chlor']
choiceValue.set('Ammoniak')
w = OptionMenu(row2, choiceValue, *choices)
row2.pack(side=TOP, fill=X, padx=5, pady=5)
labelStoff.pack(side=LEFT)
w.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row3 = Frame(container1)
labelNumbersteps = Label(row3, width=20, anchor='w', text="Anzahl Schritte*", font=("Helvetica", 13))
entryNumbersteps = Entry(row3)
row3.pack(side=TOP, fill=X, padx=5, pady=5)
labelNumbersteps.pack(side=LEFT)
entryNumbersteps.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row4 = Frame(container1)
labelTimesteps = Label(row4, width=20, anchor='w', text="Zeitabstand (min)*", font=("Helvetica", 13))
entryTimesteps = Entry(row4)
row4.pack(side=TOP, fill=X, padx=5, pady=5)
labelTimesteps.pack(side=LEFT)
entryTimesteps.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

buttonStart = Button(container1, text='Start', padx=25, pady=5, command=create)
myFont = font.Font(family='Helvetica', size=10, weight='bold')
buttonStart['font'] = myFont
buttonStart.pack(side=RIGHT, padx=5, pady=(5, 10))

container2 = Frame(window)
container2.pack(side=RIGHT, padx=(20, 20))
img = Image.open('CivilDefence.png')
newImg = img.resize((180, 180), Image.ANTIALIAS)
newImg = ImageTk.PhotoImage(newImg)
panel = Label(container2, image=newImg)
panel.pack(side=RIGHT)

mainloop()
