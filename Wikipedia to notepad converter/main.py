from tkinter import *
import wikipediaapi
import os
from tkinter import messagebox

# functions
def createdoc():
    topic = title.get()
    search_wikipedia(topic)

def clear_details():
    title.delete(0, END)

def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia('english')  

    page_py = wiki_wiki.page(query)

    if page_py.exists():
        print("Page Title:", page_py.title)
        print("Page URL:", page_py.fullurl)
        print("\nSummary:")
        
        try:
            cwd = os.path.dirname(os.path.abspath(__file__))
            with open(cwd+"\\"+query+".txt", "x", encoding="utf-8") as file:  # Specify 'utf-8' encoding
                file.write(f"Page Title: {page_py.title}\n")
                file.write(f"Page URL: {page_py.fullurl}\n\n")
                file.write("Summary:\n")
                file.write(page_py.summary[:99999])
                print(cwd)
            print(f"Data saved to {query}")
            messagebox.showinfo("Status","Process completed successfully")                
        except FileExistsError:
            print(f"File {query} already exists. Choose a different topic or delete the existing file.")
            messagebox.showinfo("Status","Process failed")
    else:
        print("Page not found.")
        messagebox.showinfo("Status","Process failed")

# GUI setup
tk = Tk()
tk.geometry("500x270")
tk.wm_resizable(False,False)
tk.title("Wikipedia to text document")

Label(tk, text="Welcome to Wikipedia to document converter", font=("bold", 16), padx=10).grid(row=0, columnspan=3)

Label(tk, text="Enter the topic in one word : ", font=("bold")).grid(row=1, column=0)
title = Entry(tk, font=("bold"))
title.grid(row=1, column=1, pady=10)

Button(tk, pady=10, text="Get data to text document", command=createdoc).grid(row=2, column=0, pady=20)
Button(tk, pady=10, text="Clear details", command=clear_details).grid(row=2, column=1, pady=20)

tk.mainloop()
