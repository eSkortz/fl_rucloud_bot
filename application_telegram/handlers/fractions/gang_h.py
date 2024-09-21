from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

from config import database_engine_async, BOT_TOKEN
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_gangs_model import Gangs
from database.orm.public_users_model import Users

from handlers.main_h import sth_error
from keyboards.fractions import gang_menu_k, calculate_confirmation_k
from utils.discord_utils import get_messages, post_without_images


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=BOT_TOKEN)


class CaptPathGroup(StatesGroup):
    waiting_to_id = State()


class CalculateSalaryGroup(StatesGroup):
    waiting_to_count = State()
    waiting_to_summ = State()


@router.callback_query(F.data == "gang_menu")
async def gang_menu(callback: CallbackQuery) -> None:
    try:
        text = (
            ">🥷 Это раздел __*Банда*__, на данный момент здесь вы можете произвести автоматический расчет "
            "зарплаты каптерам, в будущем сюда могут быть добавлены доп\. опции\."
        )
        markup_inline = gang_menu_k.get()
        await callback.message.delete()
        await callback.message.answer(
            text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data == "edit_salary_channel")
async def edit_salary_channel(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        user_in_db = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_in_db: Users = user_in_db[0]
        gang_in_db = await database_worker.custom_orm_select(
            cls_from=Gangs, where_params=[Gangs.user_id == user_in_db.id]
        )
        gang_in_db: Gangs = gang_in_db[0]

        sent_message = await callback.message.answer(
            text=(
                f">✏️ Введите новый id чата с отчетами каптов\. Текущее значение:\n```\n{gang_in_db.capt_chat_id}```\n"
                ">>Пример искомого значения: \n__https:/discord\.com/channels/1065391328889929859/__ \n\> *1192433132994048010* \<"
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(CaptPathGroup.waiting_to_id)
        await state.update_data(callback=callback)
        await state.update_data(id_to_delete=sent_message.message_id)
        await state.update_data(gang_id=gang_in_db.id)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(CaptPathGroup.waiting_to_id)
async def processing_path(message: Message, state: FSMContext) -> None:
    try:
        new_chat_id = message.text
        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        callback = state_data["callback"]
        gang_id = state_data["gang_id"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        data_to_update = {
            "id": gang_id,
            "capt_chat_id": new_chat_id,
        }
        await database_worker.custom_orm_bulk_update(cls_to=Gangs, data=[data_to_update])

        await gang_menu(callback=callback)

    except Exception as exception:
        await sth_error(message, exception)


@router.callback_query(F.data == "calculate_salary")
async def calculate_salary(callback: CallbackQuery) -> None:
    try:
        await callback.message.delete()
        markup_inline = calculate_confirmation_k.get()
        await callback.message.answer(
            text=(
                f">💰 Убедитесь, что вы хотите выполнить данное действие\. Если вы пользуетесь данной функцией в первый раз \- "
                "проверьте чтобы в сообщении, вплоть до которого будет идти расчет, присутствуют символы '\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-'\.\n\n"
                ">После введения всех нужных параметров бот отправит в канал с отчетами сообщение от вашего имени с результатами\."
            ),
            reply_markup=markup_inline,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data == "calculate_process")
async def edit_salary_channel(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        sent_message = await callback.message.answer(
            text=(
                f"ℹ️ _*Введите минимальное кол\-во каптов, начиная от которого выдается зарплата человеку:*_"
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.update_data(id_to_delete=sent_message.message_id)
        await state.update_data(callback=callback)
        await state.set_state(CalculateSalaryGroup.waiting_to_count)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(CalculateSalaryGroup.waiting_to_count)
async def processing_count(message: Message, state: FSMContext) -> None:
    try:
        count = int(message.text)
        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        sent_message = await message.answer(
            text=(f"ℹ️ _*Введите общую сумму денег на балансе:*_"),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        await state.update_data(id_to_delete=sent_message.message_id)
        await state.update_data(count=count)
        await state.set_state(CalculateSalaryGroup.waiting_to_summ)
    except Exception as exception:
        await sth_error(message, exception)


@router.message(CalculateSalaryGroup.waiting_to_summ)
async def processing_summ(message: Message, state: FSMContext) -> None:
    try:
        summ = int(message.text)
        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        count = state_data["count"]
        callback = state_data["callback"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        user_in_db = await database_worker.custom_orm_select(
            cls_from=Users, where_params=[Users.telegram_id == message.chat.id]
        )
        user_in_db: Users = user_in_db[0]
        gang_in_db = await database_worker.custom_orm_select(
            cls_from=Gangs, where_params=[Gangs.user_id == user_in_db.id]
        )
        gang_in_db: Gangs = gang_in_db[0]

        messages = await get_messages(
            authorization=user_in_db.discord_token, channel_id=gang_in_db.capt_chat_id
        )
        members = {}
        for message in messages:
            if "---------" in message["content"]:
                break
            for mention in message["mentions"]:
                if mention["id"] in members.keys():
                    members[mention["id"]] += 1
                else:
                    members[mention["id"]] = 1

        total_count = 0
        clean_members = {}
        for key, value in members.items():
            if value >= count:
                clean_members[key] = value
                total_count += value

        text = ""
        for key, value in members.items():
            text = (
                text
                + f"👤 <@{key}> - {summ / total_count * value} руб. (Отыграно {value} капт(-а/-ов))\n"
            )

        text = text + "-------------------------------\n🫦 -# Maked By SmotraAssistant"

        await post_without_images(
            authorization=user_in_db.discord_token,
            text=text,
            channel_id=gang_in_db.capt_chat_id,
        )
        await gang_menu(callback=callback)

    except Exception as exception:
        await sth_error(message, exception)
