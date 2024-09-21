from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from handlers.main_h import sth_error
from keyboards.cars import mark_menu_k
from utils.text_utils import CARS_CLASSIFICATION
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_cars_model import Cars

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("car_marks"))
async def car_marks(callback: CallbackQuery) -> None:
    try:
        car_mark = callback.data.split("|")[1]
        first_element_index = int(callback.data.split("|")[2])
        markup_inline = await mark_menu_k.get(
            car_mark=car_mark, first_element_index=first_element_index
        )
        photo = FSInputFile(f"src/cars/{car_mark}.png")
        all_cars_by_mark = await database_worker.custom_orm_select(
            cls_from=Cars, where_params=[Cars.classification == car_mark]
        )
        text = (
            f"Список автомобилей {CARS_CLASSIFICATION[car_mark]['emoji']} "
            + f"{CARS_CLASSIFICATION[car_mark]['name']} (стр. {first_element_index//5+1}/"
            + f"{len(all_cars_by_mark)//5+1 if len(all_cars_by_mark) % 5 != 0 else len(all_cars_by_mark)//5})"
        )
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo, caption=text, reply_markup=markup_inline
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
