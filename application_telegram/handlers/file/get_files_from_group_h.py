from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from keyboards.organizations import get_files_from_group_k
from keyboards.personal import personal_main_k
from aiogram.enums.parse_mode import ParseMode

router = Router()


@router.callback_query(F.data.startswith("get_files_from_group"))
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    directory_name = callback.data.split("|")[1]
    first_element_index = int(callback.data.split("|")[2])
    photo = FSInputFile("src/personal.png")
    markup_inline = await get_files_from_group_k.get(first_element_index=first_element_index, group_name=directory_name, message=callback.message)
    await callback.message.answer_photo(
        photo=photo,
        caption="> 📂 Это раздел файлов группы, здесь вы можете смотреть файлы, которые доступны вам и тем, кому предоставлен доступ\.",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2
    )
