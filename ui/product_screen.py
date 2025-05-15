import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection

class ProductScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Product Management")
        self.master.geometry("500x400")

        # Input fields
        tk.Label(master, text="Product Name").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Price").grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(master)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="Stock").grid(row=2, column=0, padx=5, pady=5)
        self.stock_entry = tk.Entry(master)
        self.stock_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(master, text="Add Product", command=self.add_product).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Edit Product", command=self.edit_product).grid(row=3, column=1, pady=10)
        tk.Button(master, text="Delete Product", command=self.delete_product).grid(row=3, column=2, pady=10)

        # Product List
        self.tree = ttk.Treeview(master, columns=("Name", "Price", "Stock"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.load_products()
        self.master.update()


        self.load_products()

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        if name == "" or price == "" or stock == "":
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number, and stock must be an integer.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully!")
        self.load_products()
    def edit_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Product", "Please select a product to edit.")
            return

        values = self.tree.item(selected, 'values')
        name, price, stock = values

        new_name = self.name_entry.get()
        new_price = self.price_entry.get()
        new_stock = self.stock_entry.get()

        if new_name == "" or new_price == "" or new_stock == "":
            messagebox.showwarning("Input Error", "All fields are required for editing.")
            return

        try:
            new_price = float(new_price)
            new_stock = int(new_stock)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be number and stock must be integer.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, price=?, stock=? WHERE name=? AND price=? AND stock=?",
                       (new_name, new_price, new_stock, name, float(price), int(stock)))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Product updated successfully!")
        self.load_products()

    def delete_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Product", "Please select a product to delete.")
            return

        values = self.tree.item(selected, 'values')
        name, price, stock = values

        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE name=? AND price=? AND stock=?", (name, float(price), int(stock)))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Product deleted successfully.")
            self.load_products()
        

    def load_products(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, stock FROM products")
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=row)

        conn.close()