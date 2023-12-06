import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, END
import pprint
import google.generativeai as palm

class ChatBot:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatBot")

        # Create chat display
        self.chat_display = Text(master, wrap="word", state="disabled")
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create scrollbar for chat display
        scrollbar = Scrollbar(master, command=self.chat_display.yview)
        scrollbar.grid(row=0, column=2, sticky="nsew")
        self.chat_display["yscrollcommand"] = scrollbar.set

        # Create user input field
        self.user_input = Entry(master, width=40)
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Create "Send" button
        send_button = Button(master, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Configure grid weights for responsiveness
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Initialize the chatbot
        self.initialize_chatbot()

    def initialize_chatbot(self):
        self.display_message("\nChatBot: Hello! How can I help you?")

    def send_message(self):
        user_message = self.user_input.get()

        if user_message:
            # Display user message in the chat
            self.display_message("\nYou: " + user_message)

            # Get and display chatbot response
            chatbot_response = self.get_chatbot_response(user_message)
            self.display_message("\nChatBot: " + chatbot_response)

            # Clear the user input field
            self.user_input.delete(0, END)

    def get_chatbot_response(self, user_message):
        try:
            # Replace with your API endpoint and key
            palm.configure(api_key='AIzaSyBtFg0uv0_CAzjXDXNdQs987wqo5z11RK4')
            models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
            model = models[0].name
            print(model)
            prompt = user_message
            completion = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0,
                # The maximum length of the response
                max_output_tokens=800,
            )

            return "\n"+completion.result+"\n"
        except Exception as e:
            print(f"Error: {e}")
            return "\nI can't understand. Please try again.\n"

    def display_message(self, message):
        # Display messages in the chat display
        self.chat_display.config(state="normal")
        self.chat_display.insert(END, message + "\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state="disabled")

def main():
    root = tk.Tk()
    root.resizable(False,False)
    chatbot_app = ChatBot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
