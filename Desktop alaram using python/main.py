import tkinter as tk
from tkinter import messagebox, simpledialog
import schedule
import time
import threading
from datetime import datetime
import winsound

tasks = {}
lock = threading.Lock()

def add_task():
    due_date_str = entry_due_date.get()

    if not due_date_str:
        messagebox.showwarning("Warning", "Please enter the due date.")
        return

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d %I:%M %p")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid date format. Please use YYYY-MM-DD hh:mm AM/PM.")
        return

    with lock:
        tasks[due_date] = due_date_str
    update_task_list()
    messagebox.showinfo("Success", f"Reminder set for {due_date}.")
    entry_due_date.delete(0, tk.END)

def edit_task():
    selected_task_index = listbox_tasks.curselection()
    if not selected_task_index:
        messagebox.showwarning("Warning", "Please select a reminder to edit.")
        return

    selected_task = listbox_tasks.get(selected_task_index)
    current_due_date = parse_task(selected_task)

    # Check if parse_task returns None
    if current_due_date is None:
        messagebox.showwarning("Warning", "Invalid task format.")
        return

    initial_value = f"{current_due_date.strftime('%Y-%m-%d %I:%M %p')}"
    # Ask for new task and due date in the specified format
    combined_input = simpledialog.askstring("Edit Task", "Enter new due date (YYYY-MM-DD hh:mm AM/PM):", initialvalue=initial_value)

    if not combined_input:
        messagebox.showwarning("Warning", "Please enter the new due date.")
        return

    try:
        new_due_date = datetime.strptime(combined_input, "%Y-%m-%d %I:%M %p")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid input format. Please use YYYY-MM-DD hh:mm AM/PM.")
        return

    with lock:
        # Update the task with the new due date
        tasks[new_due_date] = tasks.pop(current_due_date)
    update_task_list()
    messagebox.showinfo("Success", f"Reminder updated to {new_due_date}.")



def delete_task():
    selected_task_index = listbox_tasks.curselection()
    if not selected_task_index:
        messagebox.showwarning("Warning", "Please select a reminder to delete.")
        return

    with lock:
        task_to_delete = list(tasks.keys())[selected_task_index[0]]
        del tasks[task_to_delete]

    update_task_list()
    messagebox.showinfo("Success", "Reminder deleted.")

def parse_task(task_str):
    for due_date, task in tasks.items():
        formatted_due_date = due_date.strftime("%Y-%m-%d %I:%M %p")
        if formatted_due_date == task_str:
            return due_date

def update_task_list():
    with lock:
        listbox_tasks.delete(0, tk.END)
        for due_date in tasks:
            formatted_due_date = due_date.strftime("%Y-%m-%d %I:%M %p")
            listbox_tasks.insert(tk.END, formatted_due_date)


def reminder(task):
    # Show the reminder message box
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
    result = messagebox.showinfo("Reminder", f"Time to {task}!\nClick 'OK' when you're ready.")

    # Stop the reminder sound when the user clicks "OK"
    winsound.PlaySound(None, winsound.SND_ALIAS)

def check_reminders():
    current_time = datetime.now()

    with lock:
        tasks_to_remove = []
        for due_date, task in tasks.items():
            if current_time > due_date:
                reminder(f"{task}")
                tasks_to_remove.append(due_date)

        # Remove completed tasks
        for due_date in tasks_to_remove:
            del tasks[due_date]

    update_task_list()

def schedule_reminder_check():
    while True:
        schedule.run_pending()
        time.sleep(1)

# GUI setup
root = tk.Tk()
tk.re
root.title("Simple Reminder App")

label_due_date = tk.Label(root, text="Set Reminder for (YYYY-MM-DD hh:mm AM/PM):")
label_due_date.grid(row=0, column=0, padx=10, pady=10)

entry_due_date = tk.Entry(root)
entry_due_date.grid(row=0, column=1, padx=10, pady=10)

button_add_task = tk.Button(root, text="Set Reminder", command=add_task)
button_add_task.grid(row=1, column=0, pady=10, sticky="ew")

button_edit_task = tk.Button(root, text="Edit Reminder", command=edit_task)
button_edit_task.grid(row=1, column=1, pady=10, sticky="ew")

button_delete_task = tk.Button(root, text="Delete Reminder", command=delete_task)
button_delete_task.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

listbox_tasks = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=5)
listbox_tasks.grid(row=3, column=0, columnspan=2, pady=10)

# Schedule the check_reminders function to run every minute
schedule.every(1).minutes.do(check_reminders)

# Update the task list and run the scheduled task continuously in a separate thread
update_task_list_thread = threading.Thread(target=update_task_list)
update_task_list_thread.start()

reminder_check_thread = threading.Thread(target=schedule_reminder_check)
reminder_check_thread.start()

# Start the Tkinter event loop
root.mainloop()
