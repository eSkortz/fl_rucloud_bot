from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from config import database_engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_files_model import Files


database_worker = DatabaseWorkerAsync(engine=database_engine_async)


async def get(file: Files, fallback_string: str) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🗳 Загрузить файл", callback_data=f"download_file|{file.id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
