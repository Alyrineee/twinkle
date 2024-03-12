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
@dp.callback_query(F.data == "ctrl_cat")
async def feed(call: types.CallbackQuery):
    cursor.execute(f'SELECT Hungry From Cats WHERE id={call.from_user.id}')
    cat_hungry = cursor.fetchone()[0]
    cursor.execute(f'SELECT Stars From Cats WHERE id={call.from_user.id}')
    cat_stars = cursor.fetchone()[0]
    cursor.execute(f'SELECT Code From Stars WHERE Name = {call.from_user.id} AND Eat=0')
    eat_stars = cursor.fetchall()
    await bot.send_message(call.message.chat.id,
                        f"Тут ты можешь покормить своего кота\n\nКот будет есть звезды которые ты съел последними\n\nВот сколько у вашего кота очков голода: {cat_hungry}\n\nВот сколько всего у Вас звезд: {cat_stars}\n\nВот сколько Вы можете съесть: {len(eat_stars)}",
                           reply_markup=gui.ctrl_cat())


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
        while True:
            star = models.star()
            try:
                cursor.execute('INSERT INTO Stars (Code,Name,Rank,Date) VALUES (?,?,?,?)',
                               (star.code, star.name, star.rank, star.date))
                conn.commit()
                break
            except:
                temp_star = cursor.execute('SELECT code FROM Stars WHERE Code = ? AND Name = ?', (star.code, star.name))
                if tuple(*temp_star) != ():
                    break
        temp_lot = models.lot(message.chat.id,message.text)
        code = False
        cursor.execute('INSERT INTO Games (ID,Gamer_ID,Code,Winner) VALUES (?,?,?,?)',
                       (temp_lot.id, temp_lot.tg, temp_lot.code, temp_lot.winner))
        conn.commit()
        cursor.execute('SELECT Code FROM Games WHERE ID = 0')
        temp_code = cursor.fetchall()[-1][0]
        wrong = 0
        correct = 0
        print(temp_lot.tg)
        for i in range(8):
            if temp_code[i] == star.code[i]:
                correct+=1
                print(temp_code[i],star.code[i])
            else:
                wrong+=1
                print(temp_code[i], star.code[i])
        cursor.execute(f'SELECT Stars FROM Cats WHERE id={temp_lot.tg}')
        stars = cursor.fetchall()[0][0]
        print(stars)
        if correct/8 >= 0.5:
            cursor.execute(f'UPDATE Stars SET Name={temp_lot.tg} WHERE Code = "{star.code}"')
            cursor.execute(f'UPDATE Cats SET Stars={stars + 1} WHERE id = {temp_lot.tg}')
            conn.commit()
            await bot.send_message(message.chat.id, "Вы получаете 1 звезду!", reply_markup=gui.back())
        else:
            cursor.execute(f'SELECT Hungry From Cats WHERE id={temp_lot.tg}')
            cat_hungry = cursor.fetchone()[0]
            cursor.execute(f'UPDATE Cats SET Hungry={cat_hungry-(stars*wrong)//7} WHERE id = {temp_lot.tg}')
            conn.commit()
            cursor.execute(f'SELECT Hungry From Cats WHERE id={temp_lot.tg}')
            cat_hungry = cursor.fetchone()[0]
            if cat_hungry<=0:
                await bot.send_message(message.chat.id, "кот умер....")
                cursor.execute(
                    f'UPDATE Stars SET Eat=0 WHERE Name = {temp_lot.tg}')
                conn.commit()
                cursor.execute(
                    f'UPDATE Stars SET Name="None" WHERE Name = {temp_lot.tg}')
                conn.commit()
                cursor.execute(
                    f'DELETE FROM Cats WHERE id = {temp_lot.tg}')
                conn.commit()
            else:
                await bot.send_message(message.chat.id, "К сожалению вы не получаете звезду(", reply_markup=gui.back())

@dp.callback_query(F.data == "top")
async def feed(call: types.CallbackQuery):
    await call.message.answer("В разработке...",reply_markup=gui.back())

@dp.callback_query(F.data == "go_lobby")
async def class_change(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("Добро пожаловать в Twinkle\nЧем займемся сейчас?\nПодсказка: чтобы ваш кот жил ему нужны звезды!",reply_markup=gui.lobby())
@dp.callback_query(F.data == "feed_cat")
async def feed(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    cursor.execute(f'SELECT Code From Stars WHERE Name = {call.from_user.id} AND Eat=0')
    star_code = cursor.fetchall()[-1][0]
    cursor.execute(f'SELECT Rank From Stars WHERE Name ={call.from_user.id} AND Eat=0')
    star_rare = cursor.fetchall()[-1][0]
    cursor.execute(f'UPDATE Stars SET Eat=1 WHERE Code="{star_code}"')
    conn.commit()
    cursor.execute(f'SELECT Hungry From Cats WHERE id={call.from_user.id}')
    cat_hungry = cursor.fetchone()[0]
    print(cat_hungry)
    if star_rare == 'common':
        cursor.execute(f'UPDATE Cats SET Hungry={cat_hungry+(100 - cat_hungry) * 0.1} WHERE id = {call.from_user.id}')
    elif star_rare == 'rare':
        cursor.execute(f'UPDATE Cats SET Hungry={cat_hungry+(100 - cat_hungry) * 0.2} WHERE id = {call.from_user.id}')
        conn.commit()
    elif star_rare == 'epic':
        cursor.execute(f'UPDATE Cats SET Hungry={cat_hungry+(100 - cat_hungry) * 0.5} WHERE id = {call.from_user.id}')
        conn.commit()
    elif star_rare == 'legendary':
        cursor.execute(f'UPDATE Cats SET Hungry={cat_hungry+(100 - cat_hungry) * 0.9} WHERE id = {call.from_user.id}')
        conn.commit()
    await call.message.answer("Кот поел",reply_markup=gui.lobby())


@dp.callback_query(F.data == "earn_stars")
async def class_change(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(f"Упала звезда!!!\n\nЧтобы получить звезду тебе необходимо угадать как можно больше цифр в числе\n\nЭто число состоит из 8 цифр от 0 до 1\n\nФормат ответа: 00101000")
    global code
    code = True


if __name__ == "__main__":
    asyncio.run(main())