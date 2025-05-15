import tkinter as tk
from tkinter import messagebox
from ui.product_screen import ProductScreen

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("POS System - Login")
        self.master.geometry("300x200")

        tk.Label(master, text="Username").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Password").pack()
        self.password_entry = tk.Entry(master, show='*')
        self.password_entry.pack()

        tk.Button(master, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy authentication
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login", "Login successful!")
            self.master.destroy()

            new_window = tk.Tk()
            screen = ProductScreen(new_window)
            new_window.mainloop()
            # You will later open the dashboard here
        else:
            messagebox.showerror("Login", "Invalid credentials.")