from aiogram.types import ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from config import engine_async
from utils.func_utils import group_list, get_rucloud_groups_list




async def get(first_element_index: int, message: Message) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    rucloud_group_list = await get_rucloud_groups_list(message.chat.id)

    groups = await group_list(message.chat.id)

    for group in rucloud_group_list:
        groups.append(group)

    if len(groups) > first_element_index + 5:
        last_element_index = first_element_index + 5
    else:
        last_element_index = len(groups)

    for index in range(first_element_index, last_element_index):
        if not groups[index].find("ru"):
            callback_data = f"get_files_from_group|{groups[index].split(" ")[1]}|0"
        else:
            callback_data = f"test"
        builder.row(
            types.InlineKeyboardButton(
                text=f"{groups[index]}",
                callback_data=callback_data
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"organizations_main|{first_element_index - 5 if first_element_index != 0 else 0}",
        ),
        types.InlineKeyboardButton(
            text="Вперед ➡️",
            callback_data=f"organizations_main|{first_element_index + 5 if len(groups) > first_element_index + 5 else first_element_index}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Создать группу", callback_data="create_group"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад в меню", callback_data="main_menu"
        )
    )
    return builder.as_markup(resize_keyboard=True)