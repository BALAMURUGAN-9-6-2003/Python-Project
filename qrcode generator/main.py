import qrcode
import os
from tkinter import *
from tkinter import messagebox

def generate():
    data=entry.get()
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    cwd = os.path.dirname(os.path.abspath(__file__))
    print(cwd)
    
    output_filename = cwd+"\\"+entry1.get()+".png"
    img.save(output_filename)
    

    print(f"QR Code generated and saved as {output_filename}")
    messagebox.showinfo("task completed","File location is "+output_filename)

def clear():
    entry.delete(0,len(entry.get()))

if __name__ == "__main__":
    
    tk=Tk()
    tk.geometry("250x230")
    tk.title("")
    tk.resizable(False,False)
    Label(tk,text="QR Code generator",font=("Bold",18),pady=20,padx=20).grid(row=0,columnspan=2)
    Label(tk,text="Enter the text ",pady=20).grid(row=1,column=0)
    entry=Entry(tk)
    entry.grid(row=1,column=1)
    Label(tk,text="Enter the file name ",pady=20).grid(row=2,column=0)
    entry1=Entry(tk)
    entry1.grid(row=2,column=1)
    btn=Button(tk,text="generate",command=generate).grid(row=3,column=0)
    btn=Button(tk,text="clear",command=clear).grid(row=3,column=1)
    url_data = entry.get()
    tk.mainloop()
