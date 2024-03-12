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
            types.InlineKeyboardButton(text="✨ Заработать звезды", callback_data="earn_stars")
        ],
        [
            types.InlineKeyboardButton(text="😺 Управление котом", callback_data="ctrl_cat")
        ],
        [
            types.InlineKeyboardButton(text="🚀 Топ", callback_data="top")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def ctrl_cat():
    buttons = [
        [
            types.InlineKeyboardButton(text="💖Покормить", callback_data="feed_cat"),
            types.InlineKeyboardButton(text="🔙Назад", callback_data="go_lobby"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
