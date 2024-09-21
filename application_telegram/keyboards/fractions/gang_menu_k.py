from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="💰 Рассчитать зарплаты", callback_data=f"calculate_salary"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔐 Изменить Authorization токен",
            callback_data="change_authorization|gang",
        ),
        types.InlineKeyboardButton(
            text="✏️ Редактировать id канала отчетов",
            callback_data=f"edit_salary_channel",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🪪 Фракции", callback_data="fractions_main"
        )
    )
    return builder.as_markup(resize_keyboard=True)
