import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
conn = sqlite3.connect("endtermdatabase.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS tours (
    id INTEGER PRIMARY KEY,
    caption TEXT,
    start_date TEXT,
    end_date TEXT,
    price TEXT,
    img TEXT
)
''')


cursor.execute("""
           CREATE TABLE IF NOT EXISTS reserved_tours (
               id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                caption TEXT,
                start_date TEXT,
                end_date TEXT,
                price TEXT,
                img TEXT
           )
       """)
conn.commit()


def add_tour(caption,start_date,end_date,price,img):
    cursor.execute("INSERT INTO tours (caption, start_date, end_date, price, img) VALUES (?, ?, ?, ?, ?)", (caption, start_date, end_date, price, img))
    conn.commit()


def remove_tour(tour_id):
    cursor.execute("DELETE FROM tours WHERE id = ?", (tour_id,))
    conn.commit()


def get_tours():
    cursor.execute("SELECT id, name FROM tours")
    return cursor.fetchall()


