# TODO

# Möglichkeit Screenshots aus Ordner "screenshots" mit Filesystem auszuwählen und anzuzeigen
# Analog das erstellte GIF anzeigen
from tkinter import *
from tkinter import filedialog


def exitapp(window):
    window.destroy()


def opendialog(window):
    window.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("png files", "*.png"),
                                                            ("all files", "*.*")))
    showimage(window.filename)


def showimage(filename):
    imagewindow = Toplevel()
    canvas = Canvas(imagewindow, width=300, height=300)
    canvas.pack()
    img = PhotoImage(file=filename)
    canvas.create_image(20, 20, anchor=NW, image=img)
    mainloop()
