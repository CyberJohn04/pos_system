import sqlite3

# Connect to the database (make sure pos.db exists in the same folder)
conn = sqlite3.connect("pos.db")
cursor = conn.cursor()

# Add one sample product
cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
               ("Sample Product", 99.99, 20))

conn.commit()
conn.close()

print("Sample product added successfully!")