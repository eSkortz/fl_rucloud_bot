from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(number_of_gm: int, contact_link: str) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🔍 Найти ГМ",
            callback_data=f"find_rent_list|{number_of_gm}|0",
        ),
        types.InlineKeyboardButton(text="✏️ Написать арендодателю", url=contact_link),
    )
    return builder.as_markup(resize_keyboard=True)
