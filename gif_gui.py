from tkinter import *
import time


def opengif(name, gifnr):
    gifwindow = Tk()
    # gifwindow.attributes("-fullscreen", True)
    # gifwindow.bind("<Escape>", close_escape(gifwindow))

    label = Label()
    label.pack()

    counter = 0

    while counter < gifnr:

        photo = PhotoImage(file=name, format="gif -index " + str(counter))
        label.config(image=photo)
        time.sleep(1)
        gifwindow.update()
        counter += 1
        if counter == gifnr:
            counter = 0


# def close_escape(gifwindow):
#     print("escaped")
#     gifwindow.destroy()
