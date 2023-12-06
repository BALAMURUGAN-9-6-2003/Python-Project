import PyPDF2
import tkinter as tk
from tkinter import filedialog

def protect_pdf(input_path, output_path, password):
    try:
        with open(input_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()

            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            pdf_writer.encrypt(password)

            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

        status_label.config(text="PDF protected successfully!")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def browse_save_location():
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    entry_save_path.delete(0, tk.END)
    entry_save_path.insert(0, save_path)

def protect_pdf_button():
    input_path = entry_file_path.get()
    output_path = entry_save_path.get()
    password = entry_password.get()

    if input_path and output_path and password:
        protect_pdf(input_path, output_path, password)
    else:
        status_label.config(text="Please fill in all fields.")

def clear_items():
    entry_file_path.delete(0,len(entry_file_path.get()))
    entry_save_path.delete(0,len(entry_save_path.get()))
    entry_password.delete(0,len(entry_password.get()))
# Create the main window
root = tk.Tk()
root.title("PDF Protector Tool")
root.resizable(False,False)
# Create and place widgets
label_file_path = tk.Label(root, text="Select PDF file:")
label_file_path.grid(row=0, column=0, padx=10, pady=10)

entry_file_path = tk.Entry(root, width=40)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)

button_browse_file = tk.Button(root, text="Browse", command=browse_file)
button_browse_file.grid(row=0, column=2, padx=10, pady=10)

label_save_path = tk.Label(root, text="Save location:")
label_save_path.grid(row=1, column=0, padx=10, pady=10)

entry_save_path = tk.Entry(root, width=40)
entry_save_path.grid(row=1, column=1, padx=10, pady=10)

button_browse_save_location = tk.Button(root, text="Browse", command=browse_save_location)
button_browse_save_location.grid(row=1, column=2, padx=10, pady=10)

label_password = tk.Label(root, text="Enter password:")
label_password.grid(row=2, column=0, padx=10, pady=10)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=10)

button_protect_pdf = tk.Button(root, text="Protect PDF", command=protect_pdf_button)
button_protect_pdf.grid(row=3, columnspan=1, pady=20)

clear = tk.Button(root, text="Clear", command=clear_items)
clear.grid(row=3, column=2, pady=20,padx=10)

status_label = tk.Label(root, text="")
status_label.grid(row=4, column=1)

# Start the main loop
root.mainloop()
