from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from config import engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_organizations_model import Organizations


database_worker = DatabaseWorkerAsync(engine=engine_async)


async def get(organizations: List[Organizations]) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for organization in organizations:
        builder.row(
            types.InlineKeyboardButton(
                text=f"🏣 {organization.name}",
                callback_data=f"organization_menu|{organization.id}",
            )
        )

    builder.row(
        types.InlineKeyboardButton(
            text=f"➕ Создать организацию", callback_data=f"create_organization"
        )
    )

    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"main_menu"))
    return builder.as_markup(resize_keyboard=True)
