from tkinter import *
import time


def opengif(name, gifnr):
    gifwindow = Tk()

    label = Label()
    label.pack()

    counter = 0

    while counter < gifnr:

        photo = PhotoImage(file=name, format="gif -index " + str(counter))
        label.config(image=photo)
        time.sleep(2)
        gifwindow.update()
        counter += 1
        if counter == gifnr:
            counter = 0
