from aiogram.types import ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders


def get(
    folder_id: int,
    folders: List[Folders],
    files: List[Files],
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        ...

    for file in files:
        ...

    builder.row(
        types.InlineKeyboardButton(
            text="📤 Загрузить файл", callback_data=f"upload_file|{folder_id}"
        ),
        types.InlineKeyboardButton(
            text="📨 Создать папку", callback_data=f"delete_file|{folder_id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🪧 Создать рабочее пространство",
            callback_data=f"create_collaboration|{folder_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")
    )
    return builder.as_markup(resize_keyboard=True)
