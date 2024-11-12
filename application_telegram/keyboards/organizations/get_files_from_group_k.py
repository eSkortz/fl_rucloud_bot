from aiogram.types import ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from config import engine_async
from db.orm.schema_public import Users, Groups
from utils.func_utils import get_files_list
from db.oop.alchemy_di_async import DBWorkerAsync

db_worker = DBWorkerAsync(engine=engine_async)


async def get(first_element_index: int, message: Message, group_name="") -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    group_members = await db_worker.custom_orm_select(
        cls_from=Groups,
        where_params=[Groups.group_name == group_name]
    )

    owner_telegram_id = message.chat.id
    for index in range(len(group_members)):
        member: Groups = group_members[index]
        if member.is_owner & member.telegram_id != owner_telegram_id:
            owner_telegram_id = member.telegram_id
            break

    user_credits = await db_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == owner_telegram_id],
    )
    user_credits: Users = user_credits[0]
    username, password = user_credits.nextcloud_login, user_credits.nextcloud_password

    files = await get_files_list(nextcloud_login=username, nextcloud_password=password,
                                 directory_name="group_directory/" + group_name)

    last_element_index = (
        first_element_index + 5 if len(files) > first_element_index + 5 else len(files)
    )

    for index in range(first_element_index, last_element_index):
        builder.row(
            types.InlineKeyboardButton(
                text=f"{files[index]}",
                callback_data=f"file_download|group_directory/{group_name}/{files[index]}"
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"get_files_from_group|{group_name}|{first_element_index - 5 if first_element_index != 0 else 0}",
        ),
        types.InlineKeyboardButton(
            text="Вперед ➡️",
            callback_data=f"get_files_from_group|{group_name}|{first_element_index + 5 if len(files) > first_element_index + 5 else first_element_index}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Загрузить файл", callback_data="upload_file|"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад в меню", callback_data="main_menu"
        )
    )
    return builder.as_markup(resize_keyboard=True)
