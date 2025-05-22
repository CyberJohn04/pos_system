import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection

class ProductScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("POS - Product Management")
        self.master.configure(bg="#f0f2f5")

        # Labels and Entry Fields
        tk.Label(master, text="Product Name:", bg="#f0f2f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Price:", bg="#f0f2f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Entry(master)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Stock:", bg="#f0f2f5").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.stock_entry = tk.Entry(master)
        self.stock_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(master, text="Add Product", command=self.add_product, bg="#4CAF50", fg="white").grid(row=3, column=0, pady=10)
        tk.Button(master, text="Edit Product", command=self.edit_product, bg="#2196F3", fg="white").grid(row=3, column=1, pady=10)
        tk.Button(master, text="Delete Product", command=self.delete_product, bg="#f44336", fg="white").grid(row=3, column=2, pady=10)

        # Product List (Treeview)
        self.tree = ttk.Treeview(master, columns=("Name", "Price", "Stock"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.load_products()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, stock FROM products")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        if not name or not price or not stock:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number. Stock must be an integer.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully!")
        self.clear_fields()
        self.load_products()

    def edit_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Product", "Please select a product to edit.")
            return

        values = self.tree.item(selected, "values")
        old_name = values[0]

        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        if not name or not price or not stock:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number. Stock must be an integer.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name = ?, price = ?, stock = ? WHERE name = ?", (name, price, stock, old_name))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product updated successfully!")
        self.clear_fields()
        self.load_products()

    def delete_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Product", "Please select a product to delete.")
            return

        values = self.tree.item(selected, "values")
        name = values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE name = ?", (name,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Product deleted successfully.")
            self.clear_fields()
            self.load_products()

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)