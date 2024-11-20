from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config import database_engine_async, TELEGRAM_TOKEN
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Folders, M2M_UsersFolders, Users
from keyboards import only_to_main_k

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)

class FoldersGroup(StatesGroup):
    waiting_to_name = State()

# delete_folder
@router.callback_query(F.data.startswith("delete_folder"))
async def delete_folder(callback: CallbackQuery):
    folder_id = int(callback.data.split("|")[1])

    database_worker.custom_delete_all(
        cls_from=Folders,
        where_params={"id": folder_id},
    )

    await callback.message.delete()
    markup_inline = only_to_main_k.get()
    await callback.message.answer(
        text=f"Папка успешно удалена",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

# share_folder
@router.callback_query(F.data.startswith("share_folder"))
async def get_users(callback: CallbackQuery, state: FSMContext):
    folder_id = int(callback.data.split("|")[1])
    sent_message = await callback.message.answer(text="Введите имена пользователей")
    await state.set_state(FoldersGroup.waiting_to_name)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(folder_id=folder_id)

@router.message(FoldersGroup.waiting_to_name)
async def process_users(message: Message, state: FSMContext):
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]
    folder_id = state_data["folder_id"]
    users_name = message.text.split(",")

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    for user in users_name:
        user_from_db: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == user],
            get_unpacked=True,
        )

        data_to_insert = {
            "user_id": user_from_db.id,
            "folder_id": folder_id,
        }

        await database_worker.custom_insert(cls_to=M2M_UsersFolders, data=[data_to_insert])

    markup_inline = only_to_main_k.get()
    await callback.message.answer(
        text=f"Доступ перечисленным пользователям предоставлен",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


# create_folder
@router.callback_query(F.data.startswith("create_folder"))
async def delete_folder(callback: CallbackQuery):
    folder_id = int(callback.data.split("|")[1])
