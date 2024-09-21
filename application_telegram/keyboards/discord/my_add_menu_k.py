from aiogram.types import ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(chapter: str, images_number: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="⏰ Изменить таймер", callback_data=f"add_change_timer|{chapter}"
        ),
        types.InlineKeyboardButton(
            text="♻ Вкл/Выкл", callback_data=f"add_on_off|{chapter}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📝 Отредактировать текст",
            callback_data=f"add_change_text|{chapter}",
        ),
    )
    if images_number < 10:
        builder.row(
            types.InlineKeyboardButton(
                text="🎑 Добавить фото",
                callback_data=f"add_attach_photo|{chapter}",
            ),
            types.InlineKeyboardButton(
                text="🧨 Удалить все фото", callback_data=f"add_remove_photos|{chapter}"
            ),
        )
    else:
        builder.row(
            types.InlineKeyboardButton(
                text="🧨 Удалить все фото", callback_data=f"add_remove_photos|{chapter}"
            ),
        )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 📢 Мои объявления", callback_data="my_adds"
        )
    )
    return builder.as_markup(resize_keyboard=True)
