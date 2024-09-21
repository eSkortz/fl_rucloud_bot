from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_cars_model import Cars

from utils.text_utils import batch_price_generator, CARS_CLASSIFICATION


database_worker = DatabaseWorkerAsync(database_engine_async)


async def get(car_mark: str, first_element_index: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cars = await database_worker.custom_orm_select(
        cls_from=Cars,
        where_params=[Cars.classification == car_mark],
        order_by=[Cars.price],
    )
    last_element_index = (
        first_element_index + 5 if len(cars) > first_element_index + 5 else len(cars)
    )
    for index in range(first_element_index, last_element_index):
        car: Cars = cars[index]
        builder.row(
            types.InlineKeyboardButton(
                text=f"{CARS_CLASSIFICATION[car_mark]['emoji']} {car.name} {batch_price_generator(str(car.price))}",
                callback_data=f"car_info|{car.id}",
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"car_marks|{car_mark}|{first_element_index - 5 if first_element_index != 0 else 0}",
        ),
        types.InlineKeyboardButton(
            text="Вперед ➡️",
            callback_data=f"car_marks|{car_mark}|{first_element_index + 5 if len(cars) > first_element_index + 5 else first_element_index}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🚗 Автомобили", callback_data="cars_main"
        )
    )
    return builder.as_markup(resize_keyboard=True)
