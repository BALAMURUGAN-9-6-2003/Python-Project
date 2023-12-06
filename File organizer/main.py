import os
import shutil
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

tk=Tk()
tk.geometry("290x270")
tk.title("File Organizer")
tk.wm_resizable(False,False)
def folderlocation():
    t=filedialog.askdirectory()
    entry.delete(0, END)  # Clear the Entry widget
    entry.insert(0, t)

def organize_files():
    directory=entry.get()
    print(directory)
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_extension = os.path.splitext(filename)[1]
            if file_extension:
                destination_directory = os.path.join(directory, file_extension[1:])
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)
                shutil.move(os.path.join(directory, filename), os.path.join(destination_directory, filename))
    messagebox.showinfo("success","Organization completed!")

Label(tk,text="File Organizer",font=("BOLD",30),pady=16,padx=16).grid(columnspan=5,row=0)
label = Label(tk, text="Folder Location", font=("BOLD")).grid(column=0, row=1)
entry=Entry(tk)
entry.grid(column=1,row=1)
Button(tk,text="Choose Folder",padx=10,pady=10,command=folderlocation).grid(row=2,column=0)
Button(tk,text="Align files",padx=10,pady=10,command=organize_files).grid(row=2,column=1)

tk.mainloop()