from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get(car_mark: str) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text=f'🔙 В раздел {car_mark}', callback_data="cars_main"
    ))
    return builder.as_markup(resize_keyboard=True)