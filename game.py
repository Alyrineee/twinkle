from sqlite3 import Cursor

import db_controller,models,gui
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
import requests
from dotenv import load_dotenv
from os import environ
import sqlite3
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = environ["TOKEN"]

bot = Bot(token=TOKEN)
dp = Dispatcher()
global create
create = False
global code
code = False

conn = sqlite3.connect('catsandstars.s3db', check_same_thread=False)
cursor = conn.cursor()


async def main():
    await dp.start_polling(bot)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    id = cursor.execute('SELECT id FROM Cats WHERE id = ?', (message.chat.id,))
    conn.commit()
    if tuple(*id) == ():
        await bot.send_message(message.chat.id, "Добро пожаловать в Twinkle!\n\nЯ вижу что у тебя нет кота(\nДавай его создадим!",reply_markup=gui.start_keyboard())
    else:
        await bot.send_message(message.chat.id,"Добро пожаловать в Twinkle\nЧем займемся сейчас?", reply_markup=gui.lobby())

@dp.callback_query(F.data == "create_cat")
async def class_change(call: types.CallbackQuery):
    global create
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("Введи имя кота:")
    create = True

@dp.message()
async def echo_message(message: types.Message):
    global code
    global create
    if create:
        create = False
        temp_cat = models.cat(message.text, message.chat.id)
        await bot.send_message(message.chat.id,f"Имя кота: {temp_cat.name}\nГолод: {float(temp_cat.hungry)}\nЗвезды: {temp_cat.stars}\nID: {temp_cat.id}",reply_markup=gui.after_create())
        cursor.execute('INSERT INTO Cats (Name,Hungry,Stars,Id) VALUES (?,?,?,?)', (temp_cat.name,float(temp_cat.hungry),temp_cat.stars,temp_cat.id))
        conn.commit()
    if code:
        temp_lot = models.lot(message.chat.id,message.text)
        code = False
        cursor.execute('INSERT INTO Games (ID,Gamer_ID,Code,Winner) VALUES (?,?,?,?)',
                       (temp_lot.id, temp_lot.tg, temp_lot.code, temp_lot.winner))
        conn.commit()


@dp.callback_query(F.data == "go_lobby")
async def class_change(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("Добро пожаловать в Twinkle\nЧем займемся сейчас?",reply_markup=gui.lobby())



@dp.callback_query(F.data == "earn_stars")
async def class_change(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    star = models.star()
    await call.message.answer(f"Каждую минуту вам будет приходить сообщение о розыгрыше звезды.\nЧем больше вы угадаете цифр тем больше шанс получить звезду\n\nDATA:{star.name}:{star.code}:{star.rank}:{star.date}\n\nВведите код:")
    global code
    code = True



if __name__ == "__main__":
    asyncio.run(main())