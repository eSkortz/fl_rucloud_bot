from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from datetime import datetime, timedelta

from config import database_engine_async, TELEGRAM_TOKEN
from keyboards import delete_message_k

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_folders_model import Folders
from database.orm.public_m2m_users_folders_model import M2M_UsersFolders
from database.orm.public_m2m_folders_folders_model import M2M_FoldersFolders


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)


class FoldersGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_user_id = State()
    waiting_to_expire = State()


@router.callback_query(F.data.startswith("delete_folder"))
async def delete_folder(callback: CallbackQuery) -> None:
    folder_id = int(callback.data.split("|")[1])

    await database_worker.custom_delete_all(
        cls_from=Folders,
        where_params={"id": folder_id},
    )

    markup_inline = delete_message_k.get()
    await callback.message.answer(
        text=f"✅ Папка успешно удалена",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("share_folder"))
async def get_users(callback: CallbackQuery, state: FSMContext) -> None:
    folder_id = int(callback.data.split("|")[1])
    sent_message = await callback.message.answer(
        text="Введите id пользователя (любой пользователь может запросить свой id через команду /get_id)",
    )
    await state.set_state(FoldersGroup.waiting_to_user_id)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(folder_id=folder_id)


@router.message(FoldersGroup.waiting_to_user_id)
async def waiting_to_user_id(message: Message, state: FSMContext) -> None:
    user_id = int(message.text)

    sent_message = await message.answer(
        text="Введите кол-во дней, на которое хотите выдать доступ (по умолчанию 30 дней)",
    )

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    folder_id = int(state_data["folder_id"])

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    await state.set_state(FoldersGroup.waiting_to_expire)
    await state.update_data(user_id=user_id)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(folder_id=folder_id)


@router.message(FoldersGroup.waiting_to_expire)
async def waiting_to_expire(message: Message, state: FSMContext) -> None:
    try:
        expire_days = int(message.text)
    except Exception:
        expire_days = 30

    expired_at = datetime.now() + timedelta(days=expire_days)

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    folder_id = state_data["folder_id"]
    user_id = state_data["user_id"]

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == user_id],
        get_unpacked=True,
    )

    data_to_insert = {
        "user_id": user.id,
        "folder_id": folder_id,
        "is_owner": False,
        "expired_at": expired_at,
    }
    await database_worker.custom_insert(cls_to=M2M_UsersFolders, data=[data_to_insert])

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Папка успешно расшарена",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("create_folder"))
async def create_folder(callback: CallbackQuery, state: FSMContext) -> None:
    parent_folder_id = int(callback.data.split("|")[1])
    sent_message = await callback.message.answer(
        text="Введите название папки",
    )
    await state.set_state(FoldersGroup.waiting_to_name)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(parent_folder_id=parent_folder_id)


@router.message(FoldersGroup.waiting_to_name)
async def waiting_to_name(message: Message, state: FSMContext) -> None:
    name = message.text

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    parent_folder_id = state_data["parent_folder_id"]

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id],
        get_unpacked=True,
    )

    data_to_insert = {"name": name}
    await database_worker.custom_insert(cls_to=Folders, data=[data_to_insert])
    inserted_folder: Folders = await database_worker.custom_orm_select(
        cls_from=Folders,
        where_params=[Folders.name == name],
        order_by=[Folders.created_at.desc()],
        sql_limit=1,
        get_unpacked=True,
    )

    data_to_insert = {
        "parent_folder_id": parent_folder_id,
        "child_folder_id": inserted_folder.id,
    }
    await database_worker.custom_insert(
        cls_to=M2M_FoldersFolders, data=[data_to_insert]
    )

    data_to_insert = {
        "user_id": user.id,
        "folder_id": inserted_folder.id,
    }
    await database_worker.custom_insert(cls_to=M2M_UsersFolders, data=[data_to_insert])

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Папка успешно создана",
        reply_markup=markup_inline,
    )
