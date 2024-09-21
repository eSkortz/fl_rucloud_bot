from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="➰ Audi", callback_data="car_marks|audi|0"),
        types.InlineKeyboardButton(text="🌍 BMW", callback_data="car_marks|bmw|0"),
        types.InlineKeyboardButton(text="🧭 Mercedes", callback_data="car_marks|mercedes|0"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🌐 Мультибрендовые", callback_data="car_marks|multi|0"),
        types.InlineKeyboardButton(text="🛸 Лада", callback_data="car_marks|lada|0"),
        types.InlineKeyboardButton(text="🎌 Японские", callback_data="car_marks|japan|0",)
    )
    builder.row(
        types.InlineKeyboardButton(text="👑 Элитные", callback_data="car_marks|elite|0"),
        types.InlineKeyboardButton(text="🏍 Мотоциклы", callback_data="car_marks|moto|0"),
        types.InlineKeyboardButton(text="🚁 Вертолеты", callback_data="car_marks|helicopter|0",)
    )
    builder.row(
        types.InlineKeyboardButton(text="💎 Эксклюзивы", callback_data="car_marks|exclusive|0"),
        types.InlineKeyboardButton(text="🚛 Фуры", callback_data="car_marks|trucks|0",
    ))
    builder.row(types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu"))
    return builder.as_markup(resize_keyboard=True)
