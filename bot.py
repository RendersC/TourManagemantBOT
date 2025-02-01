import os
import json
import sqlite3
from database import add_tour,remove_tour,get_tours
import aiogram.types
from aiogram.types import InlineKeyboardButton
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

#Грузим джейсоны в текстс
with open("texts.json",'r',encoding="utf-8") as f:
    texts = json.load(f)


#Хендлер все туры
@dp.message_handler(text ="Все туры")
async def send_welcome(message: types.Message):
    await message.answer(texts["Все туры"],reply_markup=kb.ikb_tours)

#хендлер о нас
@dp.message_handler(text ="О нас")
async def send_welcome(message: types.Message):
    await message.answer(text=texts[message.text])

#Хендлер заброннированных туров
@dp.message_handler(text ="Забронированные туры")
async def send_welcome(message: types.Message):
    pass

#Хендлер админ-панель
@dp.message_handler(text ="Админ-панель")
async def send_welcome(message: types.Message):
    await message.answer(text="ADMIN-PANNEL",reply_markup=kb.inline_admin_btn)



#BUTTON BACK
@dp.callback_query_handler(lambda c: c.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,"Все туры: ", reply_markup=kb.ikb_tours)
    await bot.answer_callback_query(callback_query.id)


#пока что потом уберу надо создать универсальную функцию
@dp.callback_query_handler(lambda c: c.data == "1")
async def process_callback_tour_details(callback_query: types.CallbackQuery):
    await bot.send_photo(
                         callback_query.from_user.id,
                         photo=open('images/img.png', 'rb'),
                         caption='ЦЕНА: 155000\nПАКЕТ: Питание + ЭКСКУРСИЯ + ИНСТРУКТОР И ТД',
                         reply_markup=kb.backkb)
    await bot.answer_callback_query(callback_query.id)

#разработка универсальной функций
def represent_tours():
    for tour in get_tours():
        kb.ikb_tours.add(InlineKeyboardButton(tour[1],callback_data=tour[0]))








#пока что потом доработка
@dp.callback_query_handler(lambda c: c.data == "Reserve")
async def reserve(callback_query: types.CallbackQuery):
    pass







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

    # Получаем URL файла
    file_info = await bot.get_file(file_id)
    photo_url = f"https://api.telegram.org/file/bot{os.getenv('TOKEN')}/{file_info.file_path}"
    async with state.proxy() as data:
        data['img'] = photo_url
    try:
        add_tour(caption=data['caption'], start_date=data['start_date'], end_date=data['end_date'], price=data['price'],img=data['img'])
        await message.answer("Добавление тура закончен !")
    except:
        print("Ошибка в добавлений в базу данных")
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp)
