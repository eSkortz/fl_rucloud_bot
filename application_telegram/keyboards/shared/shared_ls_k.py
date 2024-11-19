from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from config import engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders


database_worker = DatabaseWorkerAsync(engine=engine_async)


async def get(
    folders: List[Folders],
    files: List[Files],
    fallback_string: str,
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📂 {folder.name}", callback_data=f"personal_ls|{folder.id}"
            )
        )

    for file in files:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📑 {file.name}", callback_data=f"personal_file_menu|{file.id}"
            )
        )
        
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
