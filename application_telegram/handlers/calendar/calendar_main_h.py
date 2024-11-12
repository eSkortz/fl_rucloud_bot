from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from keyboards.calendar import calendar_main_k
from aiogram.enums.parse_mode import ParseMode


router = Router()


@router.callback_query(F.data == "calendar_main")
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    photo = FSInputFile("src/calendar.png")
    markup_inline = calendar_main_k.get()
    await callback.message.answer_photo(
        photo=photo,
        caption="> 📆 Это раздел календаря событий, здесь вы можете распланировать свое рабочее время и поделиться им с коллегами",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2
    )
