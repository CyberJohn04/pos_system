import tkinter as tk
from tkinter import ttk
import sqlite3
from database.db import get_connection

class TransactionHistoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Transaction History")
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self, text="Transaction History", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Product ID", "Quantity", "Subtotal", "Date"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Product ID", text="Product ID")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.heading("Date", text="Date")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_transactions()

    def load_transactions(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()