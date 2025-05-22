import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class SalesScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Sales")
        self.master.geometry("800x600")
        self.conn = sqlite3.connect("pos.db")
        self.cursor = self.conn.cursor()

        self.cart = []

        # Product input
        input_frame = tk.Frame(master)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Product ID").grid(row=0, column=0)
        self.product_id_entry = tk.Entry(input_frame)
        self.product_id_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Quantity").grid(row=0, column=2)
        self.quantity_entry = tk.Entry(input_frame)
        self.quantity_entry.grid(row=0, column=3)

        add_btn = tk.Button(input_frame, text="Add to Cart", bg="#28a745", fg="white", command=self.add_to_cart)
        add_btn.grid(row=0, column=4, padx=10)

        # Cart
        self.cart_tree = ttk.Treeview(master, columns=("Name", "Qty", "Price", "Subtotal"), show="headings")
        self.cart_tree.heading("Name", text="Product")
        self.cart_tree.heading("Qty", text="Quantity")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Subtotal", text="Subtotal")
        self.cart_tree.pack(pady=10, fill="x")

        # Total Label
        self.total = 0.0
        self.total_label = tk.Label(master, text="Total: 0.00", font=("Arial", 14, "bold"))
        self.total_label.pack()

        # Buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        checkout_btn = tk.Button(btn_frame, text="Checkout", bg="#007bff", fg="white", width=15, command=self.checkout)
        checkout_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear Cart", bg="#dc3545", fg="white", width=15, command=self.clear_cart)
        clear_btn.grid(row=0, column=1, padx=5)

        manage_btn = tk.Button(btn_frame, text="Go to Product Management", bg="#ffc107", fg="black", width=25, command=self.go_to_product_management)
        manage_btn.grid(row=0, column=2, padx=5)

    def add_to_cart(self):
        product_id = self.product_id_entry.get()
        quantity = self.quantity_entry.get()

        if not product_id or not quantity.isdigit():
            messagebox.showerror("Input Error", "Please enter valid product ID and quantity")
            return

        self.cursor.execute("SELECT name, price, stock FROM products WHERE id=?", (product_id,))
        result = self.cursor.fetchone()

        if not result:
            messagebox.showerror("Not Found", "Product ID not found.")
            return

        name, price, stock = result
        quantity = int(quantity)

        if quantity > stock:
            messagebox.showerror("Stock Error", "Not enough stock available.")
            return

        subtotal = price * quantity
        self.cart_tree.insert("", tk.END, values=(name, quantity, f"{price:.2f}", f"{subtotal:.2f}"))
        self.total += subtotal
        self.total_label.config(text=f"Total: {self.total:.2f}")

        # Optional: update stock in DB immediately or wait until checkout

        self.product_id_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def checkout(self):
        if not self.cart_tree.get_children():
            messagebox.showwarning("Empty Cart", "No items in cart.")
            return

        receipt_win = tk.Toplevel(self.master)
        receipt_win.title("Receipt")
        receipt_text = tk.Text(receipt_win, width=50, height=20)
        receipt_text.pack()

        receipt_text.insert(tk.END, "       OFFICIAL RECEIPT\n")
        receipt_text.insert(tk.END, "------------------------------\n")
        receipt_text.insert(tk.END, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        total = 0.0
        for item in self.cart_tree.get_children():
            name, qty, price, subtotal = self.cart_tree.item(item, "values")
            receipt_text.insert(tk.END, f"{name} x{qty} @ {price} = {subtotal}\n")
            total += float(subtotal)

            # Update stock
            self.cursor.execute("UPDATE products SET stock = stock - ? WHERE name = ?", (int(qty), name))

        tax = total * 0.12
        grand_total = total + tax

        receipt_text.insert(tk.END, "\n------------------------------\n")
        receipt_text.insert(tk.END, f"Subtotal: {total:.2f}\n")
        receipt_text.insert(tk.END, f"Tax (12%): {tax:.2f}\n")
        receipt_text.insert(tk.END, f"Total: {grand_total:.2f}\n")
        receipt_text.insert(tk.END, "------------------------------\n")
        receipt_text.insert(tk.END, "Thank you for shopping!")

        self.conn.commit()
        self.clear_cart()

    def clear_cart(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        self.total = 0.0
        self.total_label.config(text="Total: 0.00")

    def go_to_product_management(self):
        self.master.destroy()
        root = tk.Tk()
        from ui.product_management_screen import ProductManagementScreen
        ProductManagementScreen(root)
        root.mainloop()