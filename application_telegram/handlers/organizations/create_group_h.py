from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN, engine_async
from db.orm.schema_public import Users, Groups
from handlers.main_h import main_menu
from utils.func_utils import download_file, upload_file, create_group
from db.oop.alchemy_di_async import DBWorkerAsync

router = Router()
bot = Bot(token=BOT_TOKEN)
db_worker = DBWorkerAsync(engine=engine_async)


class AddGroup(StatesGroup):
    waiting_for_group = State()
    waiting_for_users = State()


@router.callback_query(F.data.startswith("create_group"))
async def get_group(callback: CallbackQuery, state: FSMContext) -> None:
    sent_message = await callback.message.answer(text="Введите имя для новой группы")
    await state.set_state(AddGroup.waiting_for_group)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)


@router.message(AddGroup.waiting_for_group)
async def process_group(message: Message, state: FSMContext):
    group_name = message.text
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]

    user_credits = await db_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id],
    )
    user_credits: Users = user_credits[0]
    username, password = user_credits.nextcloud_login, user_credits.nextcloud_password

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    await create_group(username, password, group_name)

    owner = True
    data_to_insert = {
        "telegram_id": message.chat.id,
        "group_name": group_name,
        "is_owner": owner
    }

    await db_worker.custom_insert(cls_to=Groups, data=[data_to_insert])

    sent_message = await callback.message.answer(text="Введите никнеймы пользователей, которых вы желаете добавить")
    await state.set_state(AddGroup.waiting_for_users)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(group_name=group_name)


@router.message(AddGroup.waiting_for_users)
async def process_users(message: Message, state: FSMContext):
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]
    group_name = state_data["group_name"]
    users_name = message.text.split(",")

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    for user in users_name:
        user_data = await db_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_username == user]
        )
        user_data: Users = user_data[0]
        user_telegram_id = user_data.telegram_id

        data_to_insert = {
            "telegram_id": user_telegram_id,
            "group_name": group_name
        }

        await db_worker.custom_insert(cls_to=Groups, data=[data_to_insert])

    await main_menu(callback=callback)

#
#
# @router.callback_query(F.data.startswith("file_upload"))
# async def main_menu(callback: CallbackQuery) -> None:
#     filename = callback.data.split('|')[1]
#     await upload_file(f"C:/Downloads/{filename}", filename.replace(' ', '%20'))

