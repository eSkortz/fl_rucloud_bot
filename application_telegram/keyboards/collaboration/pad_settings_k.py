from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Сгенерировать QR для доступа", callback_data=f"get_qr"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Ограничить круг доступа", callback_data=f"make_security"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Удалить файл", callback_data=f"delete_pad"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")
    )
    return builder.as_markup(resize_keyboard=True)
