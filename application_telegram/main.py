from aiogram import Bot, Dispatcher

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TELEGRAM_TOKEN

from schedulers.auto_check_expires import auto_check_expires

from handlers import commands_h, main_h

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


async def main() -> None:
    scheduler.add_job(auto_check_expires, trigger="cron", hour=7, minute=0)
    dp.include_routers(
        commands_h.router,
        main_h.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
