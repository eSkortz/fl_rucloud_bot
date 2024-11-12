from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📂 Список моих событий", callback_data=f"test"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🏢 Запланировать событие", callback_data=f"test"
        ),
        types.InlineKeyboardButton(
            text="⚙️ Изменить видимость календаря", callback_data=f"test"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="💬 Открыть календарь в браузере",
            url="https://nextcloud.prosto-web.agency",
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")
    )
    return builder.as_markup(resize_keyboard=True)
