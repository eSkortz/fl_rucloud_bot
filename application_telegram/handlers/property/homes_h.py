from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from typing import List

from config import database_engine_async, BOT_TOKEN
from handlers.main_h import sth_error
from keyboards.property import home_menu_k, homes_list_k, only_to_homes_k

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_homes_model import Homes
from database.orm.public_users_model import Users


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=BOT_TOKEN)


class HomesGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_expenses = State()
    waiting_to_balance = State()


@router.callback_query(F.data.startswith("homes_list"))
async def homes_list(callback: CallbackQuery) -> None:
    try:
        user: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == callback.message.chat.id],
            get_unpacked=True,
        )
        homes_list: List[Homes] = await database_worker.custom_orm_select(
            cls_from=Homes,
            where_params=[Homes.user_id == user.id],
            order_by=[Homes.created_at.asc()],
        )
        markup_inline = homes_list_k.get(homes_list=homes_list)

        text = (
            ">🏘 Это раздел __*Дома*__, здесь отображаются дома находящиеся у вас во владении\.\n\n"
            ">❗️Обратите внимание, что вам автоматически будут приходить *уведомления*, когда на вашем доме будет баланс *\-400/\-450/\-500 рублей*\.\n\n"
            ">❗️В первом случае придет *одно сообщение*, в остальных бот отправит *5 сообщений* о том, что в ближайшее время дом может слететь в гос\.\n\n"
            ">❗️Актуальное баланс дома можно увидеть в меню ниже или в меню самого дома\."
        )

        await callback.message.delete()
        await callback.message.answer(
            text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("home_menu"))
async def home_menu(callback: CallbackQuery) -> None:
    try:
        home_id = int(callback.data.split("|")[1])
        home: Homes = await database_worker.custom_orm_select(
            cls_from=Homes,
            where_params=[Homes.id == home_id],
            get_unpacked=True,
        )
        markup_inline = home_menu_k.get(home=home)

        text = (
            f">🏘 *{home.name}*\n\n"
            f">__Затраты:__ *{home.expenses} руб\./день*\n"
            f">__Баланс:__ *{home.balance} руб\.*"
        )

        await callback.message.delete()
        await callback.message.answer(
            text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("home_remove"))
async def home_remove(callback: CallbackQuery) -> None:
    try:
        home_id = int(callback.data.split("|")[1])
        await database_worker.custom_delete_all(
            cls_from=Homes, where_params=[Homes.id == home_id]
        )
        await homes_list(callback=callback)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("home_balance"))
async def home_cash_out(callback: CallbackQuery) -> None:
    try:
        home_id = int(callback.data.split("|")[1])
        if home_id == 0:
            user: Users = await database_worker.custom_orm_select(
                cls_from=Users,
                where_params=[Users.telegram_id == callback.message.chat.id],
                get_unpacked=True,
            )
            home_list: List[Homes] = await database_worker.custom_orm_select(
                cls_from=Homes,
                where_params=[Homes.user_id == user.id],
                order_by=[Homes.created_at.asc()],
            )
            await database_worker.custom_orm_bulk_update(
                cls_to=Homes,
                data=[
                    {"id": home.id, "balance": home.expenses * 14} for home in home_list
                ],
            )
            await homes_list(callback=callback)
        else:
            home: Homes = await database_worker.custom_orm_select(
                cls_from=Homes, where_params=[Homes.id == home_id], get_unpacked=True
            )
            await database_worker.custom_orm_bulk_update(
                cls_to=Homes, data=[{"id": home_id, "balance": home.expenses * 14}]
            )
            await home_menu(callback=callback)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data == "add_home")
async def add_home(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await callback.message.delete()
        sent_message = await callback.message.answer(
            text="✏️ Введите название для вашего дома",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(HomesGroup.waiting_to_name)
        await state.update_data(id_to_delete=sent_message.message_id)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(HomesGroup.waiting_to_name)
async def processing_name(message: Message, state: FSMContext) -> None:
    try:
        name = message.text

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        sent_message = await message.answer(
            text="✏️ Введите размер ежедневного платежа \(целое число без точек и запятых, например \- 30000\)",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(HomesGroup.waiting_to_expenses)
        await state.update_data(id_to_delete=sent_message.message_id, name=name)
    except Exception as exception:
        await sth_error(message, exception)


@router.message(HomesGroup.waiting_to_expenses)
async def processing_expenses(message: Message, state: FSMContext) -> None:
    try:
        expenses = int(message.text)

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        sent_message = await message.answer(
            text="✏️ Введите текущий баланс дома",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(HomesGroup.waiting_to_balance)
        await state.update_data(id_to_delete=sent_message.message_id, expenses=expenses)
    except Exception as exception:
        await sth_error(message, exception)


@router.message(HomesGroup.waiting_to_balance)
async def processing_balance(message: Message, state: FSMContext) -> None:
    try:
        balance = int(message.text)

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        name = state_data["name"]
        expenses = state_data["expenses"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        user: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == message.chat.id],
            get_unpacked=True,
        )
        data_to_insert = {
            "user_id": user.id,
            "name": name,
            "expenses": expenses,
            "balance": balance,
        }
        await database_worker.custom_insert(cls_to=Homes, data=[data_to_insert])

        markup_inline = only_to_homes_k.get()
        await message.answer(
            text=("✅ Дом успешно создан"),
            reply_markup=markup_inline,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    except Exception as exception:
        await sth_error(message, exception)
