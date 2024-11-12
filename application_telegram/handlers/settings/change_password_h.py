from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN, engine_async
from db.orm.schema_public import Users
from handlers.main_h import main_menu
from utils.func_utils import change_password
from db.oop.alchemy_di_async import DBWorkerAsync

router = Router()
bot = Bot(token=BOT_TOKEN)
db_worker = DBWorkerAsync(engine=engine_async)


class AddGroup(StatesGroup):
    waiting_for_username = State()


@router.callback_query(F.data.startswith("change_password"))
async def get_dir(callback: CallbackQuery, state: FSMContext) -> None:
    sent_message = await callback.message.answer(text="Введите новый пароль")
    await state.set_state(AddGroup.waiting_for_username)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)
    # await download_file(f"C:/Downloads/{filename}", filename.replace(' ', '%20'))


@router.message(AddGroup.waiting_for_username)
async def process_directory(message: Message, state: FSMContext):
    user_credits = await db_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id]
    )
    user_credits: Users = user_credits[0]

    username = user_credits.nextcloud_login
    id = user_credits.id
    password = message.text

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    await change_password(username,password)

    data_to_update = {
        "id": id,
        # "telegram_id": user_credits.telegram_id,
        # "telegram_username":user_credits.telegram_username,
        # "nextcloud_login": user_credits.nextcloud_login,
        "nextcloud_password": password,
    }
    await db_worker.custom_orm_bulk_update(
        cls_to=Users,
        data=[data_to_update]
    )

    await main_menu(callback=callback)