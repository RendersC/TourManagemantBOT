import os
import json
import sqlite3
from aiogram.types import InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from keyboards import keyboards as kb
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)


def get_db_connection():
    conn = sqlite3.connect('endtermdatabase.db')
    return conn


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if str(message.from_user.id) == os.getenv("ADMIN_ID"):
        await message.answer("Вы авторизованы как АДМИН",reply_markup=kb.adminkb)
    else:
        await message.answer(
            "Добро пожаловать в наш тур-бот по Казахстану!",
            reply_markup=kb.kb
        )
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('''
                INSERT INTO users (user_id)
                VALUES (?)
                ''', (user_id,))
        conn.commit()
    conn.close()



@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    await message.answer(message.from_user.id)


with open("texts.json",'r',encoding="utf-8") as f:
    texts = json.load(f)


@dp.message_handler(text ="Все туры")
async def send_welcome(message: types.Message):
    await message.answer("Все туры: ",reply_markup=kb.ikb_tours)

#BUTTON BACK
@dp.callback_query_handler(lambda c: c.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,"Все туры: ", reply_markup=kb.ikb_tours)
    await bot.answer_callback_query(callback_query.id)



@dp.callback_query_handler(lambda c: c.data == "1")
async def process_callback_tour_details(callback_query: types.CallbackQuery):
    await bot.send_photo(
                         callback_query.from_user.id,
                         photo=open('images/img.png', 'rb'),
                         caption='ЦЕНА: 155000\nПАКЕТ: Питание + ЭКСКУРСИЯ + ИНСТРУКТОР И ТД',
                         reply_markup=kb.backkb.add(InlineKeyboardButton("BUY",callback_data="Купить"),
                                                    InlineKeyboardButton("Забронировать",callback_data="Reserve"),
                                                    ))
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "Reserve")
async def reserve(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,"Все туры: ", reply_markup=kb.ikb_tours)
    await bot.answer_callback_query(callback_query.id)


if __name__ == '__main__':
    executor.start_polling(dp)
