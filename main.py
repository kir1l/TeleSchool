import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import user_commands, bot_messages, handler_utils
from utils.scheduler import schedule_daily_tasks
from config_reader import config
from utils.database import db

import logging

# Logger init
logger = logging.getLogger(__name__)


async def main():
    # Создаем экземпляр бота
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    # DB
    db.init_db()

    # Logging config
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s %(module)s'
    )

    # Scheduler init
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()

    schedule_daily_tasks(scheduler, bot)

    # Routers
    dp.include_routers(
        user_commands.router,
        bot_messages.router,
        handler_utils.router
    )

    # Отключаем dpu вебхук чтоб не получать сообщения скопившиеся при остановке бота
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг чтоб получать апдейты в реальном времени без остановки
    await dp.start_polling(bot, scheduler=scheduler)

    logger.info('Bot started')


if __name__ == '__main__':
    asyncio.run(main())

