from aiogram import Router, F
from aiogram.types import CallbackQuery, input_file
from aiogram.enums.parse_mode import ParseMode

from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_users_pointers_model import UsersPointers
from database.orm.public_discord_adds_model import DiscordAdds

from handlers.main_h import sth_error
from keyboards.discord import my_add_menu_k
from utils.text_utils import CHAPTER_CLASSIFICATION, BOOL_TO_STATUS_ADDS
from utils.func_utils import combine_images


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("discord_my_add"))
async def my_add_menu(callback: CallbackQuery, chapter_name: str = None) -> None:
    try:
        if not chapter_name:
            chapter_name = callback.data.split("|")[1]

        user_id = await database_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        pointer_model = CHAPTER_CLASSIFICATION[chapter_name]["pointer_model"]
        pointer_in_db = await database_worker.custom_orm_select(
            cls_from=pointer_model, where_params=[UsersPointers.user_id == user_id]
        )
        pointer_value: bool = pointer_in_db[0]

        add_in_db = await database_worker.custom_orm_select(
            cls_from=DiscordAdds,
            where_params=[
                DiscordAdds.user_id == user_id,
                DiscordAdds.chapter == chapter_name,
            ],
        )
        add_in_db: DiscordAdds = add_in_db[0]

        markup_inline = my_add_menu_k.get(
            chapter=chapter_name, images_number=len(add_in_db.images)
        )
        photo_note = (
            "(то, что вы видите, - это склейка для удобства просмотра, "
            + "такой костыль связан с api телеграма, в дискорд отправятся "
            + "все фотографии в полноценном виде)"
        )
        text = (
            f"Мое объявление в разделе {CHAPTER_CLASSIFICATION[chapter_name]['emoji']} "
            + f"{CHAPTER_CLASSIFICATION[chapter_name]['name']}\n\n"
            + f"💡 Статус: {BOOL_TO_STATUS_ADDS[pointer_value]}\n"
            + f"⏰ Таймер: {add_in_db.timer} минут\n"
            + f"📅 Последняя отправка: {add_in_db.last_sent.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            + f"🎑 Кол-во фотографий: {len(add_in_db.images)} {photo_note if len(add_in_db.images) != 0 else ''}\n\n"
            + f"📝 Текущий текст:\n```\n{add_in_db.text[:500]}```"
        )
        await callback.message.delete()

        if add_in_db.images:
            combine_photo = combine_images(add_in_db.images)
            combine_photo_inputfile = input_file.BufferedInputFile(
                combine_photo.read(), filename="combine_photo.png"
            )
            await callback.message.answer_photo(
                photo=combine_photo_inputfile,
                caption=text,
                reply_markup=markup_inline,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await callback.message.answer(
                text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN
            )
    except Exception as exception:
        await sth_error(callback.message, exception)
