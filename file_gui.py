import os
import webbrowser
from tkinter import *
from gif_gui import opengif


def openfilegui(lengthofimages):
    window = Tk()
    window.title('Choose Files')
    # buttonopengif = Button(window, text='Open Gif', command=lambda: opengif("animation.gif", lengthofimages))
    # buttonopengif.pack(side=TOP, padx=5, pady=5)
    row1 = Frame(window)
    labelgif = Label(row1, anchor='w', text="Open Gif", font=("Helvetica", 13), padx=10, pady=10)
    button = Button(row1, text="Open Gif Here", command=openinbrowser)
    row1.pack(side=TOP, fill=X, padx=5, pady=5)
    labelgif.pack(side=LEFT)
    button.pack(side=RIGHT, expand=YES, fill=X)

    separator = Frame(window, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=10)

    row2 = Frame(window)
    labelgif = Label(row2, anchor='w', text="Choose Screenshot", font=("Helvetica", 13), padx=10, pady=10)
    row2.pack(side=TOP, fill=X, padx=5, pady=5)
    labelgif.pack(side=LEFT)

    choicevalue = StringVar(window)
    choices = getchoicesofscreenshots()
    choicevalue.set(choices[0])
    menu = OptionMenu(row2, choicevalue, *choices, command=showscreenshot)
    row2.pack(side=TOP, fill=X, padx=5, pady=5)
    menu.pack(side=RIGHT, expand=YES, fill=X)

    separator = Frame(window, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=10)

    row3 = Frame(window)
    labelgif = Label(row3, anchor='w', text="Choose Htmls", font=("Helvetica", 13), padx=10, pady=10)
    row3.pack(side=TOP, fill=X, padx=5, pady=5)
    labelgif.pack(side=LEFT)

    choicevalue2 = StringVar(window)
    choices2 = getchoicesofhtmls()
    choicevalue2.set(choices2[0])
    menu2 = OptionMenu(row3, choicevalue2, *choices2, command=showhtmls)
    row3.pack(side=TOP, fill=X, padx=5, pady=5)
    menu2.pack(side=RIGHT, expand=YES, fill=X)

    mainloop()


def openinbrowser():
    webbrowser.open_new_tab("animation.gif")


def getchoicesofscreenshots():
    mylist = []
    for filename in os.listdir("screenshots"):
        mylist.append(filename)
    return mylist


def getchoicesofhtmls():
    mylist = []
    for filename in os.listdir("html"):
        mylist.append(filename)
    return mylist


def showscreenshot(screenshot):
    for filename in os.listdir("screenshots"):
        if filename == screenshot:
            webbrowser.open_new_tab("screenshots" + "\\" + screenshot)


def showhtmls(html):
    for filename in os.listdir("html"):
        if filename == html:
            webbrowser.open_new_tab("html" + "\\" + html)


# openfilegui(2)
