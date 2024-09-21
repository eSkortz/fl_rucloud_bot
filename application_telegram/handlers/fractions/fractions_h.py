from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.main_h import sth_error
from handlers.commands_h import fractions_command


router = Router()


@router.callback_query(F.data == "fractions_main")
async def fractions_main(callback: CallbackQuery) -> None:
    try:
        await callback.message.delete()
        await fractions_command(callback.message)
    except Exception as exception:
        await sth_error(callback.message, exception)
