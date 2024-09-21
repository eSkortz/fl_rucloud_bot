from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from database.orm.public_homes_model import Homes


def get(home: Homes) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=f"♻️ Пополнил до макс. баланса",
            callback_data=f"home_balance|{home.id}",
        ),
        types.InlineKeyboardButton(
            text=f"🗑 Удалить дом", callback_data=f"home_remove|{home.id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🏘 Дома", callback_data="homes_list"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
