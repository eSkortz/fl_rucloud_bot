from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm.public_businesses_model import Businesses


def get(businesses_list: List[Businesses]) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for business in businesses_list:
        builder.row(
            types.InlineKeyboardButton(
                text=(
                    f"🏬 {business.name} {f'({business.tasks_count} зад. / {business.balance} руб.)' if business.tasks_count < 9 else '(🛑 Слетел в гос.)'}"
                ),
                callback_data=f"business_menu|{business.id}",
            )
        )
    if len(businesses_list) < 10:
        builder.row(
            types.InlineKeyboardButton(
                text=f"➕ Добавить новый бизнес", callback_data=f"add_business"
            ),
        )
    builder.row(
        types.InlineKeyboardButton(
            text=f"♻️ Выполнил задания на всех бизнесах",
            callback_data="business_refresh_tasks|0",
        ),
        types.InlineKeyboardButton(
            text=f"💸 Снял деньги со всех бизнесов",
            callback_data="business_cash_out|0",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 💸 Мое имущество", callback_data="property_main"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
