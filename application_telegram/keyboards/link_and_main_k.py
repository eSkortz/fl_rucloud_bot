from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(url: str) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬆️ Перейти к сообщению", url=f"{url}"))
    return builder.as_markup(resize_keyboard=True)
