from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from config import engine_async
from db.orm.schema_public import Users
from keyboards.start import start_k_unregistered, start_k, start_beta_k
from db.oop.alchemy_di_async import DBWorkerAsync

router = Router()
db_worker = DBWorkerAsync(engine=engine_async)


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    user_in_db = await db_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id]
    )

    if not user_in_db:
        markup_inline = start_k_unregistered.get()
    else:
        user_in_db: Users = user_in_db[0]
        nextcloud_password = user_in_db.nextcloud_password

        if not nextcloud_password.find("welcome"):
            markup_inline = start_beta_k.get()
        else:
            markup_inline = start_k.get()
    photo = FSInputFile("src/main.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "> ☁️ Это RuCloud \- сервис, созданный для хранения данных и обмена ими "
            "с коллегами по работе"
        ),
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
