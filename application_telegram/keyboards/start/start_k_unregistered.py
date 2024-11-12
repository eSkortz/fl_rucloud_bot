from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Получить временный доступ", callback_data=f"register|"
        ),
    )

    return builder.as_markup(resize_keyboard=True)
