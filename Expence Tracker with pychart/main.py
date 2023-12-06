import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expenses = {"Food": 0, "Transportation": 0, "Entertainment": 0, "Others": 0}

        self.create_widgets()

    def create_widgets(self):
        # Expense Entry
        self.label_expense = ttk.Label(self.root, text="Enter Expense:")
        self.label_expense.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_expense = ttk.Entry(self.root)
        self.entry_expense.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Category Dropdown
        self.label_category = ttk.Label(self.root, text="Select Category:")
        self.label_category.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.category_options = ["Food", "Transportation", "Entertainment", "Others"]
        self.selected_category = tk.StringVar()
        self.dropdown_category = ttk.Combobox(self.root, textvariable=self.selected_category, values=self.category_options)
        self.dropdown_category.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.dropdown_category.set("Food")

        # Add Expense Button
        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Display Expenses Button
        self.display_button = ttk.Button(self.root, text="Display Expenses", command=self.display_expenses)
        self.display_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Plot Chart Button
        self.plot_button = ttk.Button(self.root, text="Plot Chart", command=self.plot_chart)
        self.plot_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_expense(self):
        try:
            expense_amount = float(self.entry_expense.get())
            selected_category = self.selected_category.get()

            # Update expenses dictionary
            self.expenses[selected_category] += expense_amount

            messagebox.showinfo("Expense Added", f"Rs.{expense_amount:.2f} added to {selected_category} category.")

            # Clear entry
            self.entry_expense.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid expense amount.")

    def display_expenses(self):
        expense_details = "\n".join([f"{category}: Rs.{amount:.2f}" for category, amount in self.expenses.items()])
        messagebox.showinfo("Expense Details", f"Expense Details:\n{expense_details}")

    def plot_chart(self):
        labels = list(self.expenses.keys())
        values = list(self.expenses.values())

        # Plotting the pie chart
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the chart in a Tkinter window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Chart")
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
