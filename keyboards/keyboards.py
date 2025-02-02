from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import sqlite3

kb = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
kb.add(
        KeyboardButton("Горящие туры"),
        KeyboardButton("Все туры"),
        KeyboardButton("Забронированные туры"),
        KeyboardButton("О нас"))


adminkb = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
adminkb.add(
        KeyboardButton("Горящие туры"),
        KeyboardButton("Все туры"),
        KeyboardButton("Забронированные туры"),
        KeyboardButton("О нас"),
        KeyboardButton("Админ-панель"))


adminpanel = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Добавить тур")
)







backkb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_main"),InlineKeyboardButton("Забронировать",callback_data="Reserve"))
inline_admin_btn = InlineKeyboardMarkup(row_width=2)
inline_admin_btn.add(
    InlineKeyboardButton("Добавить тур",callback_data="add_tour"),
    InlineKeyboardButton("Удалить тур по ID",callback_data="delete_tour")
)
