from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, URLInputFile, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import uuid
from io import BytesIO

from config import database_engine_async, TELEGRAM_TOKEN, S3_URL

from keyboards import delete_message_k
from utils.s3.s3_worker import S3Worker

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_files_model import Files
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
s3_worker = S3Worker()
bot = Bot(token=TELEGRAM_TOKEN)


class FilesGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_file_replace = State()
    waiting_to_file_create = State()


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


@router.callback_query(F.data.startswith("replace_file"))
async def replace_file(callback: CallbackQuery, state: FSMContext) -> None:
    file_id = int(callback.data.split("|")[1])

    sent_message = await callback.message.answer(
        text="Отправьте в сообщении файл без сжатия",
    )
    await state.set_state(FilesGroup.waiting_to_file_replace)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(file_id=file_id)


@router.message(FilesGroup.waiting_to_file_replace)
async def waiting_to_file_replace(message: Message, state: FSMContext) -> None:
    document = message.document

    file = await bot.get_file(document.file_id)
    file_path = file.file_path
    buffer = BytesIO()
    await bot.download(file_path, destination=buffer)
    file_bytes = buffer.getvalue()

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    file_id = state_data["file_id"]

    file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == file_id]
    )

    s3_worker.delete_file(path=file.path)
    await s3_worker.create_file(path=file.path, content=file_bytes)

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Файл успешно заменен",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("upload_file"))
async def upload_file(callback: CallbackQuery, state: FSMContext) -> None:
    folder_id = int(callback.data.split("|")[1])

    sent_message = await callback.message.answer(
        text="Отправьте файл в сообщении без сжатия",
    )
    await state.set_state(FilesGroup.waiting_to_file_create)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(folder_id=folder_id)


@router.message(FilesGroup.waiting_to_file_create)
async def waiting_to_file_create(message: Message, state: FSMContext) -> None:
    document = message.document

    file = await bot.get_file(document.file_id)
    file_path = file.file_path
    buffer = BytesIO()
    await bot.download(file_path, destination=buffer)
    file_bytes = buffer.getvalue()

    sent_message = await message.answer(
        text="Напишите название для нового файла",
    )

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    await state.set_state(FilesGroup.waiting_to_name)
    await state.update_data(file_bytes=file_bytes)
    await state.update_data(id_to_delete=sent_message.message_id)


@router.message(FilesGroup.waiting_to_name)
async def waiting_to_name(message: Message, state: FSMContext) -> None:
    name = message.text

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    folder_id = state_data["folder_id"]
    file_bytes = state_data["file_bytes"]

    file_path = str(uuid.uuid4())

    data_to_insert = {
        "name": name,
        "path": file_path,
    }
    await database_worker.custom_insert(cls_to=Files, data=[data_to_insert])
    inserted_file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.path == file_path], get_unpacked=True
    )
    data_to_insert = {
        "file_id": inserted_file.id,
        "folder_id": folder_id,
    }
    await database_worker.custom_insert(cls_to=M2M_FilesFolders, data=[data_to_insert])

    await s3_worker.create_file(path=file_path, content=file_bytes)

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Файл успешно создан",
        reply_markup=markup_inline,
    )
