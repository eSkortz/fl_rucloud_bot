from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import Message
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_users_pointers_model import UsersPointers
from utils.text_utils import BOOL_TO_STATUS_ADDS, CHAPTER_CLASSIFICATION

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get(message: Message) -> ReplyKeyboardMarkup:

    user_id = await database_worker.custom_orm_select(
        cls_from=Users.id, where_params=[Users.telegram_id == message.chat.id]
    )
    user_id = user_id[0]
    user_pointers = await database_worker.custom_orm_select(
        cls_from=UsersPointers, where_params=[UsersPointers.user_id == user_id]
    )
    user_pointers: UsersPointers = user_pointers[0]

    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['transport']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['transport']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.transport_pointer]}"
            ),
            callback_data="discord_my_add|transport",
        ),
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['numbers']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['numbers']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.numbers_pointer]}"
            ),
            callback_data="discord_my_add|numbers",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['homes']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['homes']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.homes_pointer]}"
            ),
            callback_data="discord_my_add|homes",
        ),
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['business']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['business']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.business_pointer]}"
            ),
            callback_data="discord_my_add|business",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['clothes']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['clothes']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.clothes_pointer]}"
            ),
            callback_data="discord_my_add|clothes",
        ),
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['weapon']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['weapon']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.weapon_pointer]}"
            ),
            callback_data="discord_my_add|weapon",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['loot']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['loot']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.loot_pointer]}"
            ),
            callback_data="discord_my_add|loot",
        ),
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['services']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['services']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.services_pointer]}"
            ),
            callback_data="discord_my_add|services",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=(
                f"{CHAPTER_CLASSIFICATION['global']['emoji']} "
                + f"{CHAPTER_CLASSIFICATION['global']['name']} "
                + f"| {BOOL_TO_STATUS_ADDS[user_pointers.global_pointer]}"
            ),
            callback_data="discord_my_add|global",
        ),
        types.InlineKeyboardButton(text="♻️ Обновить статусы", callback_data="my_adds"),
    )

    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🌐 Discord", callback_data="discord_main"
        )
    )
    return builder.as_markup(resize_keyboard=True)
