import json
from tkinter import *

from PIL import ImageTk, Image
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
density = ""
bar = ""
steps = ""
endtime = ""


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
        global density
        density = 0.7714
    elif materialChoice == "Chlor":
        density = 3.215

    content = {
        "lat": latitude,
        "lon": longitude,
        "materialChoice": materialChoice,
        "density": density,
        "bar": bar,
        "endtime": endtime,
        "steps": steps
    }

    with open('data.config', 'w') as outfile:
        json.dump(content, outfile)


def set_textfield_inputs():
    global materialChoice
    global bar
    global steps
    global endtime
    materialChoice = choiceValue.get()
    bar = entryBar.get()
    endtime = entryEndtime.get()
    steps = entrySteps.get()


def create_gif():
    if entryAddress.get() and int(entryBar.get()) and int(entryEndtime.get()) and int(entrySteps.get()):

        create_json_config_file()
        window.destroy()
        producer.generatehtml()
        checkforscreenshotsdir()
        images = []
        filenames = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--window-size=820,380")
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
            numberhtml = numberhtml + int(steps)

        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('animation.gif', images, duration=3)

        openfilegui(len(images))

    else:
        if not boolean:
            show_warning()


def addtimestamp(name, time):

    from PIL import Image, ImageDraw, ImageFont

    time = time

    image = Image.open(name)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', size=45)

    (x, y) = (100, 50)
    message = str(time)
    color = 'rgb(255, 0, 0)'
    draw.text((x, y), message, fill=color, font=font)
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
choices = ['Ammoniak', 'Chlor']
choiceValue.set('Ammoniak')
w = OptionMenu(row2, choiceValue, *choices)
row2.pack(side=TOP, fill=X, padx=5, pady=5)
labelStoff.pack(side=LEFT)
w.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row3 = Frame(container1)
labelBar = Label(row3, width=15, anchor='w', text="Bar*", font=("Helvetica", 13))
entryBar = Entry(row3)
row3.pack(side=TOP, fill=X, padx=5, pady=5)
labelBar.pack(side=LEFT)
entryBar.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row4 = Frame(container1)
labelEndtime = Label(row4, width=15, anchor='w', text="Endtime*", font=("Helvetica", 13))
entryEndtime = Entry(row4)
row4.pack(side=TOP, fill=X, padx=5, pady=5)
labelEndtime.pack(side=LEFT)
entryEndtime.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

row5 = Frame(container1)
labelSteps = Label(row5, width=15, anchor='w', text="Steps*", font=("Helvetica", 13))
entrySteps = Entry(row5)
row5.pack(side=TOP, fill=X, padx=5, pady=5)
labelSteps.pack(side=LEFT)
entrySteps.pack(side=RIGHT, expand=YES, fill=X)

separator = Frame(container1, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

buttonTest = Button(container1, text='GenerateGIF', command=create_gif)
buttonTest.pack(side=RIGHT, padx=5, pady=5)

# container2 = Frame(window)
# container2.pack(side=RIGHT, padx=(15, 0))
# img = Image.open('CivilDefence.png')
# newImg = img.resize((180, 180), Image.ANTIALIAS)
# newImg = ImageTk.PhotoImage(newImg)
# panel = Label(container2, image=newImg)
# panel.pack(side=RIGHT)

mainloop()
