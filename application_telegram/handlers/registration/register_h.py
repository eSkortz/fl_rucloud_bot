import random

import requests
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from requests.auth import HTTPBasicAuth

from config import engine_async
from db.orm.schema_public import Users
from handlers.commands_h import start_command
from keyboards.personal import personal_main_k
from aiogram.enums.parse_mode import ParseMode
from db.oop.alchemy_di_async import DBWorkerAsync
from utils.func_utils import add_new_user

router = Router()
db_worker = DBWorkerAsync(engine=engine_async)
base_url = "https://nextcloud.prosto-web.agency"


@router.callback_query(F.data.startswith("register"))
async def main_menu(callback: CallbackQuery) -> None:
    telegram_id = callback.message.chat.id
    login = callback.message.chat.username
    phrase = "welcome" + str(random.randint(0,1000))
    data_to_add = {
        "telegram_id": telegram_id,
        "telegram_username": callback.message.chat.username,
        "nextcloud_login": login,
        "nextcloud_password": phrase,
    }

    await add_new_user(login, phrase)

    await db_worker.custom_insert(cls_to=Users, data=[data_to_add])

    url = base_url + f"/remote.php/dav/files/{login}/group_directory"

    response = requests.request('MKCOL', url, auth=HTTPBasicAuth(login, phrase))

    if response.status_code == 201:
        print("Директория успешно создана")
    else:
        print(f"Ошибка при создании директории: {response.status_code}")

    await callback.message.delete()
    await start_command(callback.message)
