from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


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


ikb_tours = InlineKeyboardMarkup(row_width=1)
ikb_tours.add(
        InlineKeyboardButton("Все грани Казахстана (7 дней)",callback_data="1"),
        InlineKeyboardButton("Все грани Казахстана (7 дней)",callback_data="2"),
        InlineKeyboardButton("Все грани Казахстана (7 дней)",callback_data="3"),
        InlineKeyboardButton("Все грани Казахстана (7 дней)",callback_data="4"),
        InlineKeyboardButton("Все грани Казахстана (7 дней)",callback_data="5"),
        InlineKeyboardButton("Все грани Казахстана (7 дней)",callback_data="6")
)


backkb= InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_main"))
