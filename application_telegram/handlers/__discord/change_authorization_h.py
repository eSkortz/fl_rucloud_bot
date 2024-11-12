from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

from config import engine_async, BOT_TOKEN
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users

from handlers.main_h import sth_error
from handlers.discord.discord_h import discord_main


router = Router()
db_worker = DBWorkerAsync(engine_async)
bot = Bot(token=BOT_TOKEN)


class TokenGroup(StatesGroup):
    waiting_to_token = State()


@router.callback_query(F.data.startswith("change_authorization"))
async def change_authorization(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        user_in_db = await db_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_in_db: Users = user_in_db[0]
        user_id, user_discord_token = user_in_db.id, user_in_db.discord_token

        sent_message = await callback.message.answer(
            text=(
                f"🔐 Введите новый authorization-токен. Текущее значение:\n\n```\n{user_discord_token}```"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        await state.set_state(TokenGroup.waiting_to_token)
        await state.update_data(callback=callback)
        await state.update_data(id_to_delete=sent_message.message_id)
        await state.update_data(user_id=user_id)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(TokenGroup.waiting_to_token)
async def processing_authorization(message: Message, state: FSMContext) -> None:
    try:
        new_token = message.text
        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        user_id = state_data["user_id"]
        callback = state_data["callback"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        data_to_update = {
            "id": user_id,
            "discord_token": new_token,
            "updated_at": datetime.utcnow(),
        }
        await db_worker.custom_orm_bulk_update(cls_to=Users, data=[data_to_update])

        await discord_main(callback=callback)

    except Exception as exception:
        await sth_error(message, exception)
