import sqlite3

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('processed_files.db')

# Create a table with the specified fields
conn.execute('''CREATE TABLE IF NOT EXISTS files
             (id INTEGER PRIMARY KEY,
             date_added TEXT,
             date_processed TEXT,
             file_name TEXT)''')

# Commit the changes and close the connection
print("Files database created.")
conn.commit()
conn.close()