from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(collaboration_name: str) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔗 Сгенерировать QR для доступа",
            callback_data=f"get_qr|{collaboration_name}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🗑 Удалить файл", callback_data="main_menu")
    )
    builder.row(
        types.InlineKeyboardButton(
            text="✅ Завершить работу с файлом",
            callback_data=f"save_collaboration|{collaboration_name}",
        )
    )
    return builder.as_markup(resize_keyboard=True)
