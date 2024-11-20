from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from config import database_engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_collaborations_model import Collaborations


database_worker = DatabaseWorkerAsync(engine=database_engine_async)


async def get(collaborations: List[Collaborations]) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for collaboration in collaborations:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📑 {collaboration.name}",
                callback_data=f"collaboration_menu|{collaboration.id}",
            )
        )

    builder.row(
        types.InlineKeyboardButton(
            text=f"➕ Создать область", callback_data=f"create_collaboration"
        )
    )

    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"main_menu"))
    return builder.as_markup(resize_keyboard=True)
