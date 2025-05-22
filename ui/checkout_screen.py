# ui/checkout_screen.py
import tkinter as tk
from tkinter import messagebox, ttk
from database.db import get_connection
from ui.receipt_window import show_receipt

class CheckoutScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Sales and Checkout")

        self.cart = []
        self.total = 0

        self.setup_widgets()

    def setup_widgets(self):
        tk.Label(self.master, text="Product ID:").grid(row=0, column=0)
        self.product_id_entry = tk.Entry(self.master)
        self.product_id_entry.grid(row=0, column=1)

        tk.Label(self.master, text="Quantity:").grid(row=1, column=0)
        self.qty_entry = tk.Entry(self.master)
        self.qty_entry.grid(row=1, column=1)

        tk.Button(self.master, text="Add to Cart", command=self.add_to_cart).grid(row=2, column=0, columnspan=2)

        self.cart_tree = ttk.Treeview(self.master, columns=("Name", "Qty", "Price"), show="headings")
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Total Price")
        self.cart_tree.grid(row=3, column=0, columnspan=2)

        self.total_label = tk.Label(self.master, text="Total: ₱0.00")
        self.total_label.grid(row=4, column=0, columnspan=2)

        tk.Button(self.master, text="Checkout", command=self.checkout).grid(row=5, column=0, columnspan=2)

    def add_to_cart(self):
        try:
            product_id = int(self.product_id_entry.get())
            quantity = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid numbers")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, stock FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()

        if not product:
            messagebox.showerror("Error", "Product not found")
            return

        name, price, stock = product
        if stock < quantity:
            messagebox.showwarning("Stock Warning", "Not enough stock available.")
            return

        total_price = price * quantity
        self.cart.append((name, quantity, total_price, product_id))

        self.cart_tree.insert("", "end", values=(name, quantity, f"₱{total_price:.2f}"))
        self.total += total_price
        self.total_label.config(text=f"Total: ₱{self.total:.2f}")

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Cart Empty", "Add items first.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Update stocks
        for name, qty, total_price, pid in self.cart:
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, pid))

        # Save transaction
        item_summary = "; ".join(f"{name} x{qty}" for name, qty, _, _ in self.cart)
        cursor.execute("INSERT INTO transactions (items, total) VALUES (?, ?)", (item_summary, self.total))
        conn.commit()
        conn.close()

        show_receipt(self.master, self.cart, self.total)

        # Reset cart
        self.cart = []
        self.cart_tree.delete(*self.cart_tree.get_children())
        self.total = 0
        self.total_label.config(text="Total: ₱0.00")