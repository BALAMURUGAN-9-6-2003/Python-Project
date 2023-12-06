import tkinter as tk
from tkinter import messagebox, simpledialog
import schedule
import time
from datetime import datetime, timedelta
import threading

tasks = {}
lock = threading.Lock()

def add_task():
    task = entry_task.get()
    due_date = entry_due_date.get()

    if not task or not due_date:
        messagebox.showwarning("Warning", "Please enter both task and due date.")
        return

    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d %I:%M %p")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid date format. Please use YYYY-MM-DD hh:mm AM/PM.")
        return

    with lock:
        tasks[task] = due_date
    update_task_list()
    messagebox.showinfo("Success", f"Task '{task}' added with due date {due_date}.")
    entry_task.delete(0, tk.END)
    entry_due_date.delete(0, tk.END)

def edit_task():
    selected_task_index = listbox_tasks.curselection()
    if not selected_task_index:
        messagebox.showwarning("Warning", "Please select a task to edit.")
        return

    selected_task = listbox_tasks.get(selected_task_index)
    current_task, current_due_date = parse_task(selected_task)

    # Combine task and due date in a single string for initial value
    initial_value = f"{current_task} (Due: {current_due_date.strftime('%Y-%m-%d %I:%M %p')})"

    combined_input = simpledialog.askstring("Edit Task", "Enter new task and due date (YYYY-MM-DD hh:mm AM/PM):", initialvalue=initial_value)

    if not combined_input:
        messagebox.showwarning("Warning", "Please enter both task and due date.")
        return

    # Extract new task and due date from the combined input
    new_task, _, new_due_date_str = combined_input.partition("(Due: ")
    new_task = new_task.strip()
    
    try:
        new_due_date = datetime.strptime(new_due_date_str[:-1], "%Y-%m-%d %I:%M %p")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid date format. Please use YYYY-MM-DD hh:mm AM/PM.")
        return

    with lock:
        del tasks[current_task]
        tasks[new_task] = new_due_date
    update_task_list()
    messagebox.showinfo("Success", f"Task '{current_task}' updated to '{new_task}' with due date {new_due_date}.")


def delete_task():
    selected_task_index = listbox_tasks.curselection()
    if not selected_task_index:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        return

    # Get the selected task from the listbox
    selected_task = listbox_tasks.get(selected_task_index)

    # Extract the task name from the selected task string
    task, _ = selected_task.split("(Due: ")
    task = task.strip()

    with lock:
        del tasks[task]

    update_task_list()
    messagebox.showinfo("Success", f"Task '{task}' deleted.")

def parse_task(task_str):
    task, _, due_date_str = task_str.partition("(Due: ")
    task = task.strip()
    due_date = datetime.strptime(due_date_str[:-1], "%Y-%m-%d %I:%M %p")
    return task, due_date

def update_task_list():
    with lock:
        listbox_tasks.delete(0, tk.END)
        for task, due_date in tasks.items():
            formatted_due_date = due_date.strftime("%Y-%m-%d %I:%M %p")
            listbox_tasks.insert(tk.END, f"{task} (Due: {formatted_due_date})")

def reminder(task):
    # Show the reminder message box
    messagebox.showinfo("Reminder", f"Don't forget to '{task}'!")

def check_reminders():
    current_time = datetime.now()

    with lock:
        tasks_to_remove = []
        for task, due_date in tasks.items():
            if current_time > due_date:
                reminder(task)
                tasks_to_remove.append(task)

        # Remove completed tasks
        for task in tasks_to_remove:
            del tasks[task]

    update_task_list()

def schedule_reminder_check():
    while True:
        schedule.run_pending()
        time.sleep(1)

# GUI setup
root = tk.Tk()
root.title("To-Do List with Reminders")

label_task = tk.Label(root, text="Task:")
label_task.grid(row=0, column=0, padx=10, pady=10)

entry_task = tk.Entry(root)
entry_task.grid(row=0, column=1, padx=10, pady=10)

label_due_date = tk.Label(root, text="Due Date (YYYY-MM-DD hh:mm AM/PM):")
label_due_date.grid(row=1, column=0, padx=10, pady=10)

entry_due_date = tk.Entry(root)
entry_due_date.grid(row=1, column=1, padx=10, pady=10)

button_add_task = tk.Button(root, text="Add Task", command=add_task)
button_add_task.grid(row=2, column=0, columnspan=2, pady=10)

button_edit_task = tk.Button(root, text="Edit Task", command=edit_task)
button_edit_task.grid(row=3, column=0, columnspan=2, pady=10)

button_delete_task = tk.Button(root, text="Delete Task", command=delete_task)
button_delete_task.grid(row=4, column=0, columnspan=2, pady=10)

listbox_tasks = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=10)
listbox_tasks.grid(row=5, column=0, columnspan=2, pady=10)

# Schedule the check_reminders function to run every minute
schedule.every(1).minutes.do(check_reminders)

# Update the task list and run the scheduled task continuously in a separate thread
update_task_list_thread = threading.Thread(target=update_task_list)
update_task_list_thread.start()

reminder_check_thread = threading.Thread(target=schedule_reminder_check)
reminder_check_thread.start()

# Start the Tkinter event loop
root.mainloop()
