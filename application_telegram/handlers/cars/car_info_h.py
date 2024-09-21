from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from handlers.main_h import sth_error
from keyboards.cars import car_info_k
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_cars_model import Cars
from utils.text_utils import generate_car_info_text

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("car_info"))
async def car_marks(callback: CallbackQuery) -> None:
    try:
        car_id = int(callback.data.split("|")[1])
        car_in_db = await database_worker.custom_orm_select(
            cls_from=Cars, where_params=[Cars.id == car_id]
        )
        car_in_db: Cars = car_in_db[0]

        all_cars_by_mark = await database_worker.custom_orm_select(
            cls_from=Cars,
            where_params=[Cars.classification == car_in_db.classification],
            order_by=[Cars.price],
        )
        for index in range(len(all_cars_by_mark)):
            car: Cars = all_cars_by_mark[index]
            if car.id == car_in_db.id:
                car_index_by_price = index
                break
        page_index = car_index_by_price // 5 * 5

        markup_inline = car_info_k.get(
            car_mark=car_in_db.classification, page_index=page_index
        )
        photo = FSInputFile(car_in_db.image_link)
        text = generate_car_info_text(car_model=car_in_db)
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo, caption=text, reply_markup=markup_inline
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
