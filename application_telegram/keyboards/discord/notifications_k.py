from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(tags_list: list) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for tag in tags_list:
        builder.row(
            types.InlineKeyboardButton(
                text=f"🔊 {tag}",
                callback_data=f"none",
            ),
        )
    if len(tags_list) < 10:
        builder.row(
            types.InlineKeyboardButton(
                text="➕ Добавить тег",
                callback_data=f"add_tag",
            ),
        )
    builder.row(
        types.InlineKeyboardButton(
            text="🗑 Очистить теги",
            callback_data=f"clear_tags",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🌐 Discord", callback_data="discord_main"
        )
    )
    return builder.as_markup(resize_keyboard=True)
