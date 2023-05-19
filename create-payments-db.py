import sqlite3

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('payments.db')

# Create a table with the specified fields
conn.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY,
             account TEXT NOT NULL,
             token TEXT NOT NULL,
             amount REAL NOT NULL,
             memo TEXT,
             time_entered TEXT NOT NULL,
             time_paid TEXT,
             txid TEXT)''')

# Commit the changes and close the connection
print("Payments database created.")
conn.commit()
conn.close()