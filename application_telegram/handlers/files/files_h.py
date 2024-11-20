from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import database_engine_async, TELEGRAM_TOKEN, S3_URL

from keyboards import delete_message_k
from utils.s3.s3_worker import S3Worker

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Files

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
s3_worker = S3Worker()
bot = Bot(token=TELEGRAM_TOKEN)


class FoldersGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_user_id = State()
    waiting_to_expire = State()


@router.callback_query(F.data.startswith("download_file"))
async def download_file(callback: CallbackQuery) -> None:
    file_id = callback.data.split("|")[1]
    file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == file_id]
    )
    file = URLInputFile(f"{S3_URL}/{file.path}")

    markup_inline = delete_message_k.get()
    await callback.message.answer_document(
        document=file,
        caption=f"✅ Файл успешно удален",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("delete_file"))
async def delete_file(callback: CallbackQuery) -> None:
    file_id = int(callback.data.split("|")[1])
    file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == file_id]
    )

    await database_worker.custom_delete_all(
        cls_from=Files,
        where_params={"id": file_id},
    )
    s3_worker.delete_file(path=file.path)

    markup_inline = delete_message_k.get()
    await callback.message.answer(
        text=f"✅ Файл успешно удален",
        reply_markup=markup_inline,
    )


# replace_file
# upload_file
