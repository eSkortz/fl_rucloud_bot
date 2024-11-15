import qrcode
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile

from config import ETHERPAD_URL
from keyboards import only_to_main_k

router = Router

@router.callback_query(F.data == "get_qr")
async def generate_qr_code(callback: CallbackQuery) -> None:
    # Создаём QR-код
    qr = qrcode.QRCode(
        version=1,  # Размер QR-кода (1 - минимальный, 40 - максимальный)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
        box_size=10,  # Размер одной "коробки" в пикселях
        border=4,  # Толщина рамки (в коробках)
    )
    qr.add_data(ETHERPAD_URL)
    qr.make(fit=True)

    # Генерация изображения
    img = qr.make_image(fill_color="black", back_color="white")

    await callback.message.delete()
    markup_inline = only_to_main_k.get()
    await callback.message.answer_photo(
        photo=img,
        caption="Вот ваш QR",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2
    )