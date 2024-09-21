from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.main_h import sth_error
from keyboards.discord import my_adds_k

router = Router()


@router.callback_query(F.data == "my_adds")
async def my_adds(callback: CallbackQuery) -> None:
    try:
        await callback.message.delete()
        markup_inline = await my_adds_k.get(callback.message)
        await callback.message.answer(
            text='📢 Мои объявления (раздел|статус)',
            reply_markup=markup_inline
        )
    except Exception as exception:
        await sth_error(callback.message, exception)