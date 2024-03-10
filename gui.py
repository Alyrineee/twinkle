import models
from aiogram import Bot, Dispatcher, types

def start_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="🐈Создать кота", callback_data="create_cat")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def after_create():
    buttons = [
        [
            types.InlineKeyboardButton(text="✅Начать играть", callback_data="go_lobby")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def back():
    buttons = [
        [
            types.InlineKeyboardButton(text="🔙Назад", callback_data="go_lobby")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def lobby():
    buttons = [
        [
            types.InlineKeyboardButton(text="✨ Заработать звезды", callback_data="earn_stars"),
            types.InlineKeyboardButton(text="😺 Управление котом", callback_data="ctrl_cat"),
            types.InlineKeyboardButton(text="🚀 Топ", callback_data="top"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cat():
    print(f'Cat`s name: {cat_obj.name}')
    print(f'Stars: {cat_obj.stars}')
    print(f'Hungry: {cat_obj.hungry}')
    print('\n\n1 - Feed\n2 - Go home')
    temp = input('Select mode:')
    if temp == '1':
        star = starss.pop()
        if star.rank == 'common':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.1
        elif star.rank == 'rare':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.2
        elif star.rank == 'epic':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.5
        elif star.rank == 'legendary':
            cat_obj.hungry += (100 - cat_obj.hungry) * 0.9
