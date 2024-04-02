from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_sub_callback_button():
    keyboard = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='подписаться', callback_data='sub')
    keyboard.add(btn1)
    return keyboard.as_markup()


def get_unsub_callback_button():
    keyboard = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='отписаться от этого товара', callback_data='unsub')
    keyboard.add(btn1)
    return keyboard.as_markup()