from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=f"🔙 Назад к 🥷 Банда", callback_data=f"gang_menu"
        ),
        types.InlineKeyboardButton(
            text="✅ Продолжить", callback_data=f"calculate_process"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
