from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from config import database_engine_async, TELEGRAM_TOKEN
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Files
from keyboards import only_to_main_k

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)

# download_file
@router.callback_query(F.data.startswith("download_file"))
async def download_file(callback: CallbackQuery) -> None:
    file_id = callback.data.split("|")[1]

# replace_file

# delete_file
@router.callback_query(F.data.startswith("delete_file"))
async def delete_file(callback: CallbackQuery) -> None:
    file_id = callback.data.split("|")[1]

    database_worker.custom_delete_all(
        cls_from=Files,
        where_params={"id": file_id},
    )

    await callback.message.delete()
    markup_inline = only_to_main_k.get()
    await callback.message.answer(
        text=f"Файл успешно удален",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

# share_file