import sqlite3


conn = sqlite3.connect("endtermdatabase.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,
    reserved_orders TEXT
)
''')

conn.commit()
conn.close()