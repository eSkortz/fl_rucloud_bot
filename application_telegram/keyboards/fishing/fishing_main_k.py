from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🌊 0-5 метров", callback_data="fish_info|0"),
        types.InlineKeyboardButton(text="🌊 5-15 метров", callback_data="fish_info|5"),
        types.InlineKeyboardButton(
            text="🌊 15-25 метров", callback_data="fish_info|15"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🌊 25-45 метров", callback_data="fish_info|25"
        ),
        types.InlineKeyboardButton(
            text="🌊 45-65 метров", callback_data="fish_info|45"
        ),
        types.InlineKeyboardButton(
            text="🌊 65-85 метров", callback_data="fish_info|65"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu"),
        types.InlineKeyboardButton(
            text="🌊 от 85 метров", callback_data="fish_info|85"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
