import tkinter as tk
from tkinter import ttk
import requests

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        # Variables
        self.amount_var = tk.DoubleVar()
        self.from_currency_var = tk.StringVar()
        self.to_currency_var = tk.StringVar()
        self.result_var = tk.StringVar()

        # Entry widgets
        amount_entry = ttk.Entry(root, textvariable=self.amount_var, width=15)
        amount_entry.grid(row=0, column=0, padx=10, pady=10)

        # Combobox for currency selection
        self.from_currency_combobox = ttk.Combobox(root, textvariable=self.from_currency_var, values=[])
        self.to_currency_combobox = ttk.Combobox(root, textvariable=self.to_currency_var, values=[])

        self.from_currency_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.to_currency_combobox.grid(row=0, column=2, padx=10, pady=10)

        # Label for result
        result_label = ttk.Label(root, textvariable=self.result_var, font=('Helvetica', 14))
        result_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Button to perform conversion
        convert_button = ttk.Button(root, text="Convert", command=self.convert_currency)
        convert_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Initialize currencies
        self.initialize_currencies()

    def initialize_currencies(self):
        # Get a list of available currencies from the API
        url = "https://v6.exchangerate-api.com/v6/e555e7bff479bce81ddd60ef/latest/USD"
        response = requests.get(url)
        data = response.json()
        currencies = list(data["conversion_rates"].keys())

        # Set values for comboboxes
        self.from_currency_var.set("USD")
        self.to_currency_var.set("EUR")
        self.from_currency_combobox["values"] = currencies
        self.to_currency_combobox["values"] = currencies

    def convert_currency(self):
        try:
            # Get the conversion rates from the API
            from_currency = self.from_currency_var.get().upper()
            to_currency = self.to_currency_var.get().upper()
            
            amount = self.amount_var.get()

            url = f"https://v6.exchangerate-api.com/v6/e555e7bff479bce81ddd60ef/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()

            # Update result label
            result = amount * data["conversion_rates"][to_currency]
            self.result_var.set(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")
        except Exception as e:
            self.result_var.set("Error fetching conversion data.")

if __name__ == "__main__":
    root = tk.Tk()
    converter = CurrencyConverter(root)
    root.mainloop()
