from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🍺 Семья", callback_data=f"family_menu"),
        types.InlineKeyboardButton(text="🥷 Банда", callback_data=f"gang_menu"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu"),
    )
    return builder.as_markup(resize_keyboard=True)
