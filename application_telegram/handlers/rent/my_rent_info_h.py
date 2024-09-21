from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode

from handlers.main_h import sth_error
from keyboards.rent import my_rent_info_k

from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_rent_adds_model import RentAdds
from database.orm.public_users_model import Users


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("my_rent_info"))
async def my_rent_info(callback: CallbackQuery) -> None:
    try:
        rent_add_id = int(callback.data.split("|")[1])

        user_id = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        user_rent_add = await database_worker.custom_orm_select(
            cls_from=RentAdds, where_params=[RentAdds.id == rent_add_id]
        )
        user_rent_add: RentAdds = user_rent_add[0]
        markup_inline = my_rent_info_k.get(rent_add_id=rent_add_id)

        await callback.message.delete()
        await callback.message.answer(
            text=(
                f"🏡 (id{user_rent_add.id})\n\n"
                + f"🧱 Кол-во гаражных мест: {user_rent_add.number_of_gm}\n"
                + f"📑 Текст объявления: \n```\n{user_rent_add.add_text}```\n"
                + f"🪪 Контактная ссылка: \n```\n{user_rent_add.contact_link}```\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=markup_inline,
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
