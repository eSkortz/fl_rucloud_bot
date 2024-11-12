from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from keyboards.personal import personal_main_k
from aiogram.enums.parse_mode import ParseMode

router = Router()


@router.callback_query(F.data.startswith("personal_main"))
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    directory_name = callback.data.split("|")[1]
    first_element_index = int(callback.data.split("|")[2])
    photo = FSInputFile("src/personal.png")
    markup_inline = await personal_main_k.get(first_element_index=first_element_index,message=callback.message,directory_name=directory_name)
    await callback.message.answer_photo(
        photo=photo,
        caption="> 📂 Это раздел личных файлов, здесь вы можете хранить файлы, которыми не планируте делиться с коллегами\.",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2
    )
