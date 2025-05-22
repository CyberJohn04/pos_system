from tkinter import *
from ui.main_menu import MainMenu

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        Label(master, text="Username").grid(row=0)
        Label(master, text="Password").grid(row=1)

        self.username_entry = Entry(master)
        self.password_entry = Entry(master, show='*')

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        Button(master, text='Login', command=self.login).grid(row=2, column=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Sample authentication for now
        if username == "admin" and password == "admin":
            self.master.destroy()
            from ui.main_menu import MainMenu
            root = Tk()
            MainMenu(root, username)  # Pass username here
            root.mainloop()
        else:
            from tkinter import messagebox
            messagebox.showerror("Login Failed", "Invalid credentials")