import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE expenses (description TEXT, category TEXT, date TEXT,price REAL) 
""")

conn.commit()

conn.close()