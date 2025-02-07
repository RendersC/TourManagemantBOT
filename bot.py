import os
import re
import json
import sqlite3
from database import add_tour,remove_tour,get_tours,get_id_for_callback, get_especial_tour,add_to_reserved_tours,get_reserved_tours
import aiogram.types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from keyboards import keyboards as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)


#Грузим конфиденциальные данные и опреляем дп с ботом
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot,storage=storage)


#Фунццкция которая возвращает коннект
def get_db_connection():
    conn = sqlite3.connect('endtermdatabase.db')
    return conn


class Form(StatesGroup):
    caption = State()
    start_date = State()
    end_date = State()
    price = State()
    img = State()


class Delete_tour_cls(StatesGroup):
    delete_tour_state = State()


#Старт хендлер
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if str(message.from_user.id) == os.getenv("ADMIN_ID"):
        await message.answer("Вы авторизованы как АДМИН",reply_markup=kb.adminkb)
        await bot.send_photo(chat_id=message.from_user.id, photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRz2I8nhTQ5rSF_V1Nhl5JNpbmx-ecchrBlGg&s")
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


#Функция определений ID
@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    await message.answer(message.from_user.id)


#Грузим джейсоны в текст
with open("texts.json",'r',encoding="utf-8") as f:
    texts = json.load(f)


#чтобы репрезентировать все туры извлекая из БД
def get_fresh_tours():
    ikb_tours = InlineKeyboardMarkup(row_width=1)
    for tour in get_tours():
        ikb_tours.add(InlineKeyboardButton(tour[1],callback_data=tour[0]))
    return ikb_tours


#Универсальный колбэк хендлер для всех туров вывод характеристической информаций
@dp.callback_query_handler(lambda c: c.data.isdigit() and int(c.data) in get_id_for_callback())
async def handle_tour_callback(callback_query: CallbackQuery):
    chahacteristics = get_especial_tour(int(callback_query.data))
    repr_it = f"Описание: {chahacteristics[0]}\nВремя старта: {chahacteristics[1]}\nВремя оканчание: {chahacteristics[2]}\nЦена: {chahacteristics[3]}"
    res_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Забронировать",callback_data=f"{callback_query.data}reserve")
    )
    await bot.send_photo(callback_query.from_user.id, caption=repr_it, photo=chahacteristics[4],reply_markup=res_kb)
    await bot.answer_callback_query(callback_query.id)



#пока что потом доработка
@dp.callback_query_handler(lambda c:c.data[-1:-8:-1] == "evreser")
async def reserve(callback_query: types.CallbackQuery):
   try:
       match = re.match(r"^\d+", callback_query.data)
       if match:
           tour_id = match.group()
           add_to_reserved_tours(int(callback_query.from_user.id), tour_id)
           await bot.send_message(callback_query.from_user.id,
                                  "Тур успешно забронирован чтобы узнать по подробнее напишите вашему тур агенту @turarbek")
       else:
           await bot.send_message(callback_query.from_user.id, "Ошибка: не удалось извлечь ID тура.")
   except Exception as e:
       await bot.send_message(callback_query.from_user.id,"ВЫ УЖЕ ЗАБРОНИРОВАЛИ ЭТОТ ТУР СМОТРИТЕ В РАЗДЕЛЕ -ЗАБРОНИРОВАННЫЕ ТУРЫ-")
   finally:
       await bot.answer_callback_query(callback_query.id)



#Хендлер все туры
@dp.message_handler(text ="Все туры")
async def send_welcome(message: types.Message):
    await message.answer(texts["Все туры"],reply_markup=get_fresh_tours())


#хендлер о нас
@dp.message_handler(text ="О нас")
async def about(message: types.Message):
    await message.answer(text=texts[message.text])


#Хендлер заброннированных туров
@dp.message_handler(text ="Забронированные туры")
async def show_reserved_tours(message: types.Message):
    tours_id = get_reserved_tours(message.from_user.id)
    repr_btns = InlineKeyboardMarkup()
    for id in tours_id:
        print(id[0])#1 2 3
        tour = get_especial_tour(id[0])
        print(tour)
        repr_btns.add(InlineKeyboardButton(tour[0],callback_data=id[0]))
    await message.answer("Вот ваши заброннированные туры: ",reply_markup=repr_btns)


#Хендлер админ-панель
@dp.message_handler(text ="Админ-панель")
async def send_welcome(message: types.Message):
    await message.answer(text="ADMIN-PANNEL",reply_markup=kb.inline_admin_btn)


#BUTTON BACK
@dp.callback_query_handler(lambda c: c.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,texts["Все туры"], reply_markup=get_fresh_tours())
    await bot.answer_callback_query(callback_query.id)


#колбэк куери для Добавить тур надо сделать ввод данных
@dp.callback_query_handler(lambda c: c.data == "add_tour")
async def add_tour_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,"ДОБАВЛЯЕМ ДАННЫЕ \nВВЕДИТЕ описание:")
    await Form.caption.set()
    await bot.answer_callback_query(callback_query.id)


#Добавляем описание
@dp.message_handler(state=Form.caption)
async def add_caption(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['caption'] = message.text
    await message.answer("Введите начало тура по типу [dd:mm;yy]")
    await Form.start_date.set()


#Добавляем стартувую дату
@dp.message_handler(state=Form.start_date)
async def add_start_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['start_date'] = message.text
    await message.answer("Введите конец тура по типу [dd:mm;yy]")
    await Form.end_date.set()


#Добавляем конец тура
@dp.message_handler(state=Form.end_date)
async def add_end_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['end_date'] = message.text
    await message.answer("Введите PRICE")
    await Form.price.set()


#Добавляем цену
@dp.message_handler(state=Form.price)
async def add_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Отправьте картинку")
    await Form.img.set()


#Фианльная добавка фоты и пуш в БД
@dp.message_handler(state=Form.img,content_types= aiogram.types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    # Получаем file_id фотографии
    file_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['img'] = file_id
    try:
        add_tour(caption=data['caption'], start_date=data['start_date'], end_date=data['end_date'], price=data['price'],img=data['img'])
        await message.answer("Добавление тура закончен !")
    except:
        print("Ошибка в добавлений в базу данных")
    await state.finish()


#Колбэк для удалений тура
@dp.callback_query_handler(lambda c: c.data == "delete_tour")
async def delete_tour(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,"Введите ID записи в базы данных чтобы удалить запись")
    await Delete_tour_cls.delete_tour_state.set()
    await bot.answer_callback_query(callback_query.id)


#Принимаем ID тура
@dp.message_handler(state=Delete_tour_cls.delete_tour_state)
async def delete_tour(message: types.Message, state: FSMContext):
    tour_id = message.text
    print(tour_id)
    try:
        remove_tour(tour_id)
        print(f"Тур с ID {tour_id} успешно удалён.")
        await message.answer(f"Тур с ID {tour_id} успешно удалён.")
    except Exception as e:
        print(f"Ошибка при удалении тура: {e}")
        await message.answer(f"Ошибка при удалении тура: {e}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)

