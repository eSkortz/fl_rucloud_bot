from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import database_engine_async, BOT_TOKEN
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_rent_adds_model import RentAdds

from handlers.main_h import sth_error
from keyboards.rent import find_rent_info_k, find_rent_list_k


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=BOT_TOKEN)


class FindRentGroup(StatesGroup):
    waiting_to_gm = State()


@router.callback_query(F.data == "find_rent")
async def find_rent(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        sent_message = await callback.message.answer(
            text=(f"🔍 Введите кол-во гм, которое хотите найти, например '9' или '15'"),
        )
        await state.set_state(FindRentGroup.waiting_to_gm)
        await state.update_data(callback=callback)
        await state.update_data(id_to_delete=sent_message.message_id)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("find_rent_list"))
async def find_rent_list(
    callback: CallbackQuery, number_of_gm: int = None, page: int = None
) -> None:
    try:
        if not number_of_gm and not page:
            number_of_gm = int(callback.data.split("|")[1])
            page = int(callback.data.split("|")[2])

        user_id = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        rent_add_list = await database_worker.custom_orm_select(
            cls_from=RentAdds, where_params=[RentAdds.number_of_gm == number_of_gm]
        )

        markup_inline = find_rent_list_k.get(rent_add_list=rent_add_list, page=page)
        await callback.message.delete()
        await callback.message.answer(
            text=(f"🔍 Список объявлений по вашему запросу:"),
            reply_markup=markup_inline,
        )

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("find_rent_info"))
async def find_rent_info(callback: CallbackQuery) -> None:
    try:
        rent_add_id = int(callback.data.split("|")[1])

        user_id = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        rent_add_in_db = await database_worker.custom_orm_select(
            cls_from=RentAdds, where_params=[RentAdds.id == rent_add_id]
        )
        rent_add: RentAdds = rent_add_in_db[0]

        markup_inline = find_rent_info_k.get(
            number_of_gm=rent_add.number_of_gm, contact_link=rent_add.contact_link
        )
        await callback.message.delete()
        await callback.message.answer(
            text=(
                f"🏡 (id{rent_add.id})\n\n"
                + f"🧱 Кол-во гаражных мест: {rent_add.number_of_gm}\n"
                + f"📑 Текст объявления: \n```\n{rent_add.add_text}```\n"
                + f"🪪 Контактная ссылка: \n```\n{rent_add.contact_link}```\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=markup_inline,
        )

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(FindRentGroup.waiting_to_gm)
async def processing_gm(message: Message, state: FSMContext) -> None:
    try:
        number_of_gm = int(message.text)
        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        callback: CallbackQuery = state_data["callback"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        if number_of_gm < 1 or number_of_gm > 36:
            await callback.message.delete()
            raise ValueError(
                "Кол-во гм, которое вы указали меньше 1 или больше 36, то есть выходит за допустимые лимиты"
            )

        await find_rent_list(callback=callback, number_of_gm=number_of_gm, page=0)

    except Exception as exception:
        await sth_error(message, exception)
