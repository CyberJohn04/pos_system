# ui/receipt_window.py
import tkinter as tk
from tkinter import ttk
import datetime

def show_receipt(parent, cart, total):
    receipt_window = tk.Toplevel(parent)
    receipt_window.title("Official Receipt")

    tk.Label(receipt_window, text="OFFICIAL RECEIPT", font=("Arial", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(receipt_window, columns=("Name", "Qty", "Price"), show="headings")
    tree.heading("Name", text="Product")
    tree.heading("Qty", text="Quantity")
    tree.heading("Price", text="Price")
    tree.pack(padx=10, pady=10)

    for name, qty, total_price, _ in cart:
        tree.insert("", "end", values=(name, qty, f"\u20B1{total_price:.2f}"))

    tk.Label(receipt_window, text=f"Total Amount: \u20B1{total:.2f}", font=("Arial", 12, "bold"))
    tk.Label(receipt_window, text=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").pack()

    receipt_window.geometry("400x400")
    receipt_window.transient(parent)
    receipt_window.grab_set()
    receipt_window.mainloop()