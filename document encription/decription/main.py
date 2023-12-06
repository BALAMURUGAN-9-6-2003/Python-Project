import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet

class FileEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor/Decryptor")
        self.root.geometry("400x200")

        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

        # Create labels and buttons
        self.label = tk.Label(root, text="Select a file:")
        self.label.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_file)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt_file)
        self.decrypt_button.pack(pady=5)

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    data = file.read()
                    encrypted_data = self.cipher.encrypt(data)

                with open(file_path + ".encrypted", 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)

                tk.messagebox.showinfo("Success", "File encrypted successfully.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to decrypt")

        if file_path:
            try:
                with open(file_path, 'rb') as encrypted_file:
                    encrypted_data = encrypted_file.read()
                    decrypted_data = self.cipher.decrypt(encrypted_data)

                with open(file_path[:-10], 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

                tk.messagebox.showinfo("Success", "File decrypted successfully.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptor(root)
    root.mainloop()
