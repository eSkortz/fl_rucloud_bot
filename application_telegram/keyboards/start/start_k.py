from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📂 Личные файлы", callback_data=f"personal_main"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="📣 Общий доступ", callback_data=f"share_main"),
        types.InlineKeyboardButton(
            text="🏣 Файлы организации", callback_data=f"organizations_main"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
