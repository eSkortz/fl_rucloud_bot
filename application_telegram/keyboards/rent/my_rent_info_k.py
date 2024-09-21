from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(rent_add_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🏘 Мои объявления (ГМ)", callback_data="my_rents"
        ),
        types.InlineKeyboardButton(
            text="🗑 Удалить объявление", callback_data=f"delete_rent_add|{rent_add_id}"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
