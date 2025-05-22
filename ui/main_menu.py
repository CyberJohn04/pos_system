# ui/main_menu.py

import tkinter as tk
from ui.sales_screen import SalesScreen
from ui.product_management_screen import ProductManagementScreen

class MainMenu:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Main Menu")

        tk.Label(master, text=f"Welcome, {username}", font=("Arial", 16)).pack(pady=20)
        tk.Button(master, text="Go to Sales", command=self.open_sales).pack(pady=10)
        tk.Button(master, text="Manage Products", command=self.open_product_management).pack(pady=10)

    def open_sales(self):
        self.master.destroy()
        root = tk.Tk()
        SalesScreen(root)
        root.mainloop()

    def open_product_management(self):
        self.master.destroy()
        root = tk.Tk()
        ProductManagementScreen(root)
        root.mainloop()