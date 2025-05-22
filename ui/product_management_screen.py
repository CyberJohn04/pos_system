import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ui.sales_screen import SalesScreen  # <-- ensure this import exists

class ProductManagementScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Product Management")
        self.master.geometry("600x550")
        self.master.configure(bg="#f0f2f5")

        self.conn = sqlite3.connect("pos.db")
        self.cursor = self.conn.cursor()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=25, font=("Arial", 10))

        # Input fields
        form_frame = tk.Frame(master, bg="#f0f2f5")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Product Name", bg="#f0f2f5").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Price", bg="#f0f2f5").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.price_entry = tk.Entry(form_frame, width=30)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Stock", bg="#f0f2f5").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.stock_entry = tk.Entry(form_frame, width=30)
        self.stock_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(master, bg="#f0f2f5")
        btn_frame.pack(pady=10)

        add_btn = tk.Button(btn_frame, text="Add Product", bg="#28a745", fg="white", width=15, command=self.add_product)
        add_btn.grid(row=0, column=0, padx=5)

        edit_btn = tk.Button(btn_frame, text="Edit Product", bg="#ffc107", fg="black", width=15, command=self.edit_product)
        edit_btn.grid(row=0, column=1, padx=5)

        delete_btn = tk.Button(btn_frame, text="Delete Product", bg="#dc3545", fg="white", width=15, command=self.delete_product)
        delete_btn.grid(row=0, column=2, padx=5)

        # Product table
        self.tree = ttk.Treeview(master, columns=("ID", "Name", "Price", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200)
        self.tree.column("Price", width=100, anchor="e")
        self.tree.column("Stock", width=100, anchor="center")
        self.tree.pack(pady=10, padx=10, fill="x")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.refresh_tree()

        # Go to Sales Button (NOW correctly inside __init__)
        go_to_sales_btn = tk.Button(master, text="Go to Sales", bg="#007bff", fg="white", font=("Arial", 12), command=self.go_to_sales)
        go_to_sales_btn.pack(pady=10)

    def go_to_sales(self):
        self.master.destroy()
        root = tk.Tk()
        SalesScreen(root)
        root.mainloop()

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()
        if not name or not price or not stock:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid price or stock")
            return
        self.cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        self.conn.commit()
        self.refresh_tree()
        self.clear_fields()

    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Product", "Please select a product to edit")
            return
        item = self.tree.item(selected)
        product_id = item["values"][0]
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid price or stock")
            return
        self.cursor.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?", (name, price, stock, product_id))
        self.conn.commit()
        self.refresh_tree()
        self.clear_fields()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Product", "Please select a product to delete")
            return
        product_id = self.tree.item(selected)["values"][0]
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()
        self.refresh_tree()
        self.clear_fields()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            values = item["values"]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, values[2])
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, values[3])

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM products")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)