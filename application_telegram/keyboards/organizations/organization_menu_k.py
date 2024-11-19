from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from config import engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_organizations_model import Organizations


database_worker = DatabaseWorkerAsync(engine=engine_async)


async def get(organization: Organizations, is_owner: bool) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text=f"📂 Файлы организации",
            callback_data=f"organization_ls|0|{organization.id}",
        ),
    )

    if is_owner:
        builder.row(
            types.InlineKeyboardButton(
                text=f"👥 Добавить участника",
                callback_data=f"share_organization|{organization.id}",
            ),
            types.InlineKeyboardButton(
                text=f"🗑 Удалить организацию",
                callback_data=f"delete_organization|{organization.id}",
            ),
        )

    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"organizations_list")
    )
    return builder.as_markup(resize_keyboard=True)
