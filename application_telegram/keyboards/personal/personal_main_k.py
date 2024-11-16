from aiogram.types import ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from config import engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders


database_worker = DatabaseWorkerAsync(engine=engine_async)


async def get(
    message: Message,
    folders: List[Folders],
    files: List[Files],
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text="Загрузить файл", callback_data="upload_file"),
        types.InlineKeyboardButton(text="Создать папку", callback_data="delete_file"),
        types.InlineKeyboardButton(
            text="📤 Создать рабочее пространство", callback_data="create_collaboration"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")
    )
    return builder.as_markup(resize_keyboard=True)
