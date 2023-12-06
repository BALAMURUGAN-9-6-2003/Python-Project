#Before start the program you want to install some modules
#pip install pyttsx3
#pip install PyPdf2
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pyttsx3
import PyPDF2
import os

# Function for Playing
def play():
    text = book_name.get()
    if text:
        try:
            book = open(text, "rb")
            pdf_reader = PyPDF2.PdfReader(book)
            num_pages = len(pdf_reader.pages)
            #**********************************************
            #*Instalition of the Text to speech convector**
            #**********************************************
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[x.get()].id)
            engine. setProperty("rate", 170) 
            #**************************************
            #*Here is the Reading part of the pdf**
            #**************************************
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                print(text)
                engine.say(text)
                engine.runAndWait()
            messagebox.showinfo("Message", "Please select next book.")

        except Exception as e:
            print("Error:", e)
            message_label.config(text="Error: " + str(e), fg="red")
    else:
        message_label.config(text="Please choose a PDF file first.", fg="red")

# Function to save the audio
def save():
    text = book_name.get()
    if text:
        try:
            book = open(text, "rb")
            pdf_reader = PyPDF2.PdfReader(book)
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[x.get()].id)
            engine. setProperty("rate", 170) 

            te=""        
            for page in pdf_reader.pages:
                t = page.extract_text()
                if t and t.strip():  # Check if the extracted text is not empty or whitespace
                    te+=t

            #***********************************************
            #*Code to save the audio with the program file**
            #***********************************************
            
            cwd = os.path.dirname(os.path.abspath(__file__))
            print(cwd)
            engine.save_to_file(te, cwd+"\\"+entry.get()+".mp3")
            messagebox.showinfo("Message", "Audio Created Successfully.")

            engine.runAndWait()

        except Exception as e:
            print("Error:", e)
            message_label.config(text="Error: " + str(e), fg="red")

    else:
        message_label.config(text="Please choose a PDF file first.", fg="red")

# Function to find the file location

#***********************************************
#*Geting the location of the PDF**
#***********************************************

def getdir():
    filepath = filedialog.askopenfilename(title="Choose a PDF file", filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")))
    if filepath:
        book_name.delete(0, END)  # Clear the Entry widget
        book_name.insert(0, filepath)
        message_label.config(text="", fg="black")


#******************************************************************************************
#****************** It is the area to see the lable and button 
#******************************************************************************************
tk = Tk()
tk.title("Book Reader")
tk.geometry("500x250")
tk.wm_resizable(False,False)

heading = Label(tk, text="Welcome to Audio Converter", font=("Arial", 14, "bold"))
heading.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

Label(tk, text="PDF File Path:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
book_name = Entry(tk, width=30)
book_name.grid(row=1, column=1, padx=10, pady=10)
file = Button(tk, command=getdir, text="Choose PDF File")
file.grid(row=1, column=2)

label_voice = Label(tk, text="Choose Voice:", font=("Arial", 12))
label_voice.grid(row=2, column=0, padx=10, pady=10)

gender = ["Male", "Female"]
x = IntVar()

for i in range(2):
    Radiobutton(tk, text=gender[i], variable=x, value=i).grid(row=2, column=i + 1, padx=5, pady=10)

Label(tk,text="Enter the file name :").grid(row=3,column=0)
entry=Entry(tk)
entry.grid(row=3,column=1)
btn1 = Button(tk, text="Save Audio", command=save, bg='lightblue', font=("Arial", 12))
btn1.grid(row=4, column=1, padx=10, pady=10)

btn2 = Button(tk, text="Play Audio", command=play, bg='lightgreen', font=("Arial", 12))
btn2.grid(row=4, column=2, padx=10, pady=10)

message_label = Label(tk, text="", font=("Arial", 12))
message_label.grid(row=5, column=0, columnspan=3)

tk.mainloop()
