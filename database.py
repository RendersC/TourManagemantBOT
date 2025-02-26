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


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE
)
''')



cursor.execute("""
           CREATE TABLE IF NOT EXISTS reserved_tours (
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               tour_id TEXT 
           )
       """)
conn.commit()

def add_to_reserved_tours(user_id,tour_id):
    cursor.execute("INSERT INTO reserved_tours (user_id,tour_id) VALUES (?, ?)", (user_id,tour_id))
    conn.commit()

def get_reserved_tours(user_id):
    cursor.execute("SELECT tour_id FROM reserved_tours WHERE user_id = ?", (user_id,))
    tours = cursor.fetchall()
    print(tours)
    return tours


def add_tour(caption,start_date,end_date,price,img):
    cursor.execute("INSERT INTO tours (caption, start_date, end_date, price, img) VALUES (?, ?, ?, ?, ?)", (caption, start_date, end_date, price, img))
    conn.commit()


def remove_tour(tour_id):
    cursor.execute("DELETE FROM tours WHERE id = ?", (tour_id,))
    conn.commit()


def get_tours():
    cursor.execute("SELECT id, caption FROM tours")
    return cursor.fetchall()

def get_id_for_callback():
    cursor.execute("SELECT id FROM tours")
    return [row[0] for row in cursor.fetchall()]


def get_especial_tour(id):
    cursor.execute(
        "SELECT caption, start_date, end_date, price, img FROM tours WHERE id = ?",
        (id,)
    )

    return cursor.fetchone()


def is_tour_reserved(user_id, tour_id):
    cursor.execute("SELECT 1 FROM reserved_tours WHERE user_id = ? AND tour_id = ?", (user_id, tour_id))
    result = cursor.fetchone()
    return result is not None



