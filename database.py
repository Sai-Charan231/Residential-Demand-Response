import sqlite3

# Connect to (or create) the SQLite database file named database.db
conn = sqlite3.connect('database.db')

# Create 'users' table using schema commands
schema_sql = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
);
"""

conn.executescript(schema_sql)
conn.commit()
conn.close()

print("SQLite database and 'users' table created successfully.")
