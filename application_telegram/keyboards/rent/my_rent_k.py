from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from database.orm.public_rent_adds_model import RentAdds


def get(rent_adds_list: list) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for rent_add in rent_adds_list:
        rent_add: RentAdds
        builder.row(
            types.InlineKeyboardButton(
                text=f"🏡 (id{rent_add.id}) {rent_add.number_of_gm} гм",
                callback_data=f"my_rent_info|{rent_add.id}",
            ),
        )
    if len(rent_adds_list) < 10:
        builder.row(
            types.InlineKeyboardButton(
                text="➕ Добавить объявление", callback_data="add_rent_add"
            ),
        )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🏠 Аренда ГМ", callback_data="rent_main"
        )
    )
    return builder.as_markup(resize_keyboard=True)
