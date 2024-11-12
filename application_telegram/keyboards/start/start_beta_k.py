from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📂 Доступные файлы", callback_data=f"personal_main||0"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🏢 Мои организации", callback_data=f"organizations_main|0"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="⚙️ Настройки аккаунта", callback_data=f"settings_main"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Создать совместное рабочее пространство",
            url="https://etherpad.prosto-web.agency/",
        )
    )
    return builder.as_markup(resize_keyboard=True)
