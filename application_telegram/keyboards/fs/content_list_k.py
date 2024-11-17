from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders


def get(
    folder_id: int, folders: List[Folders], files: List[Files], callback: str
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.row(
            types.InlineKeyboardButton(
                text=f"🗂 {folder.name}",
                callback_data=f"folder_content|{folder_id}",
            ),
        )

    for file in files:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📄 {file.name}",
                callback_data=f"file_menu|{file.id}",
            ),
        )

    builder.row(
        types.InlineKeyboardButton(
            text="📤 Загрузить файл", callback_data=f"upload_file|{folder_id}"
        ),
        types.InlineKeyboardButton(
            text="📨 Создать папку", callback_data=f"create_folder|{folder_id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🪧 Создать рабочее пространство",
            callback_data=f"create_collaboration|{folder_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{callback}")
    )
    return builder.as_markup(resize_keyboard=True)
