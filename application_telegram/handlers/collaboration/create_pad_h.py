from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from keyboards.collaboration import pad_settings_k

router = Router()


@router.callback_query(F.data == "create_pad")
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    photo = FSInputFile("src/main.png")
    markup_inline = pad_settings_k.get()
    await callback.message.answer_photo(
        photo=photo,
        caption="Пространство создано, теперь вы можете его настроить",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2
    )