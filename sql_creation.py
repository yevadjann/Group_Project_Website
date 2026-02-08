import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("db.sqlite")

# Create a cursor object
cursor = conn.cursor()

# Create a sample table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

