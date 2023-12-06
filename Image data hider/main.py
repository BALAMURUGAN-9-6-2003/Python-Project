from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb

root = Tk()
root.title("Data hider using image")
root.geometry("700x500+150+180")
root.resizable(FALSE, FALSE)
root.configure(bg="#2f4155")

filename = ""
secret = None

def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select Image File",
                                          filetypes=(("PNG File", "*.png"),
                                                     ("JPG File", "*.jpg"),
                                                     ("All Files", "*.txt")))
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lbl.config(image=img, width=250, height=250)
    lbl.image = img

def hide():
    message = text1.get(1.0, END)
    global secret
    secret = lsb.hide(str(filename), message)

def show():
    clear_msg = lsb.reveal(filename)
    text1.delete(1.0, END)
    text1.insert(END, clear_msg)

def save():
    t = str(filedialog.asksaveasfilename(filetypes=(("PNG File", "*.png"),
                                                     ("JPG File", "*.jpg"),
                                                     ("All Files", "*.txt"))))
    secret.save(t + ".png")

def clear():
    global filename, secret
    filename = ""
    secret = None
    lbl.config(image="")
    text1.delete(1.0, END)

image_icon = PhotoImage(file="G:\\120 day project\\Image data hider\\logo1.jpg")
root.iconphoto(False, image_icon)

logo = PhotoImage(file="G:\\120 day project\\Image data hider\\logo.png")
Label(root, image=logo, bg="#2f4155").place(x=10, y=10)
Label(root, text="Image Data Hider", bg="#2d4155", fg="white", font="arial 25 bold ").place(x=100, y=20)
Button(root, text="Clear", width=10, height=2, font="arial 13 bold", command=clear).place(x=550, y=20)
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

Frame2 = Frame(root, bd=3, width=340, height=280, bg="White", relief=GROOVE)
Frame2.place(x=350, y=80)

text1 = Text(Frame2, font="Roboto 15", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(Frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

Frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
Frame3.place(x=10, y=370)

Button(Frame3, text="Open image", width=10, height=2, font="arial 13 bold", command=showimage).place(x=20, y=30)
Button(Frame3, text="Save image", width=10, height=2, font="arial 13 bold", command=save).place(x=180, y=30)


Label(Frame3, text="Picture, Image, Photo File", bg="#2f4155", fg="Yellow").place(x=20, y=5)

Frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
Frame4.place(x=360, y=370)

Button(Frame4, text="Hide data", width=10, height=2, font="arial 13 bold", command=hide).place(x=20, y=30)
Button(Frame4, text="Show data", width=10, height=2, font="arial 13 bold", command=show).place(x=180, y=30)

Label(Frame4, text="Picture, Image, Photo File", bg="#2f4155", fg="Yellow").place(x=20, y=5)

root.mainloop()
