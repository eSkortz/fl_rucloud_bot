from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm.public_folders_model import Folders


def get(
    folders: List[Folders],
    fallback_string: str,
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📂 {folder.name}", callback_data=f"shared_ls|{folder.id}"
            )
        )

    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
