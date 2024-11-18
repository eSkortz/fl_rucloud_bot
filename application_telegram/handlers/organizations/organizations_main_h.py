import requests
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from keyboards.organizations import organization_menu_k
from aiogram.enums.parse_mode import ParseMode


router = Router()


@router.callback_query(F.data.startswith("organizations_main"))
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    first_element_index = int(callback.data.split("|")[1])
    photo = FSInputFile("src/organizations.png")
    markup_inline = await organization_menu_k.get(first_element_index, callback.message)
    await callback.message.answer_photo(
        photo=photo,
        caption="> 📂 Это раздел организаций, из него вы можете попасть в рабочую область любой из ваших организаций\.",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2
    )
