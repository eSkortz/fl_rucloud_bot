from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode

from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_fishing_model import Fishing

from handlers.main_h import sth_error
from keyboards.fishing import only_to_fishing_k


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("fish_info"))
async def fishing_info(callback: CallbackQuery) -> None:
    try:
        depth_tag = int(callback.data.split("|")[1])
        text = await database_worker.custom_orm_select(
            cls_from=Fishing.text, where_params=[Fishing.depth == depth_tag]
        )
        text = text[0]
        markup_inline = only_to_fishing_k.get()
        await callback.message.delete()
        await callback.message.answer(
            text=text,
            reply_markup=markup_inline,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
