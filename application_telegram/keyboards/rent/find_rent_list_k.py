from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from database.orm.public_rent_adds_model import RentAdds


def get(rent_add_list: int, page: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    last_index = (
        page * 10 + 10 if page * 10 + 10 < len(rent_add_list) else len(rent_add_list)
    )
    for index in range(page * 10, last_index):
        rent_add: RentAdds = rent_add_list[index]
        builder.row(
            types.InlineKeyboardButton(
                text=f"🏡 (id{rent_add.id}) {rent_add.number_of_gm} гм",
                callback_data=f"find_rent_info|{rent_add.id}",
            ),
        )
    if rent_add_list:
        rent_add: RentAdds = rent_add_list[0]
        if page != 0 and page * 10 + 10 < len(rent_add_list):
            builder.row(
                types.InlineKeyboardButton(
                    text="◀️ Назад",
                    callback_data=f"find_rent_list|{rent_add.number_of_gm}|{page-1}",
                ),
                types.InlineKeyboardButton(
                    text="Вперед ▶️",
                    callback_data=f"find_rent_list|{rent_add.number_of_gm}|{page+1}",
                ),
            )
        elif page != 0:
            builder.row(
                types.InlineKeyboardButton(
                    text="◀️ Назад",
                    callback_data=f"find_rent_list|{rent_add.number_of_gm}|{page-1}",
                ),
            )
        elif page * 10 + 10 < len(rent_add_list):
            builder.row(
                types.InlineKeyboardButton(
                    text="Вперед ▶️",
                    callback_data=f"find_rent_list|{rent_add.number_of_gm}|{page+1}",
                )
            )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🏠 Аренда ГМ", callback_data="rent_main"
        )
    )
    return builder.as_markup(resize_keyboard=True)
