from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

from config import database_engine_async, BOT_TOKEN
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_notifications_model import Notifications

from handlers.main_h import sth_error
from keyboards.discord import notifications_k


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=BOT_TOKEN)


class NotificationGroup(StatesGroup):
    waiting_to_tag = State()


@router.callback_query(F.data == "notifications")
async def notifications(callback: CallbackQuery) -> None:
    try:
        user_id_in_db = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id_in_db[0]

        tags_in_db = await database_worker.custom_orm_select(
            cls_from=Notifications, where_params=[Notifications.user_id == user_id]
        )
        tags_list = [tag_model.tag for tag_model in tags_in_db]

        markup_inline = notifications_k.get(tags_list=tags_list)

        await callback.message.delete()
        await callback.message.answer(
            text="🔔 Мои уведомления (максимальное кол-во уведомлений - 10)",
            reply_markup=markup_inline,
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data == "clear_tags")
async def clear_tags(callback: CallbackQuery) -> None:
    try:
        user_id_in_db = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id_in_db[0]

        await database_worker.custom_orm_delete(
            cls_from=Notifications, where_params=[Notifications.user_id == user_id]
        )

        await notifications(callback)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data == "add_tag")
async def add_tag(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        sent_message = await callback.message.answer(text="🔊 Введите новый тег")

        await state.set_state(NotificationGroup.waiting_to_tag)
        await state.update_data(callback=callback)
        await state.update_data(id_to_delete=sent_message.message_id)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(NotificationGroup.waiting_to_tag)
async def processing_tag(message: Message, state: FSMContext) -> None:
    try:
        new_tag = message.text
        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        callback = state_data["callback"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        user_id_in_db = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == message.chat.id],
        )
        user_id = user_id_in_db[0]

        data_to_insert = {
            "user_id": user_id,
            "tag": new_tag,
        }
        await database_worker.custom_insert_do_nothing(
            cls_to=Notifications,
            index_elements=["user_id", "tag"],
            data=[data_to_insert],
        )

        await notifications(callback)

    except Exception as exception:
        await sth_error(message, exception)
