"""
Этот код представляет собой главную точку входа для приложения Telegram-бота. Он настраивает необходимые компоненты, включая бота, диспетчер, соединения с базой данных и middleware. Основная функция `main()` отвечает за запуск бота и обработку входящих обновлений.

Бот использует следующие компоненты:

- aiogram 3 версии: Фреймворк для Telegram-ботов на Python.
- redis.asyncio: Асинхронный клиент Redis для Python.
- motor.motor_asyncio: Асинхронный драйвер MongoDB для Python.

Основная функциональность бота обрабатывается различными маршрутизаторами (routers), которые включены в диспетчер. Эти маршрутизаторы обрабатывают команды пользователей, регистрацию, сообщения бота и взаимодействие с меню.

Бот также использует два компонента middleware:

- AntiFloodMiddleware: Реализует ограничение скорости для предотвращения злоупотребления.
- CheckRegistrationMiddleware: Проверяет регистрацию пользователя перед обработкой его запросов.

Бот запускается вызовом `asyncio.run(main())`, который запускает функцию `main()` в асинхронном цикле событий.
"""

import asyncio

from aiogram import Bot, Dispatcher
import redis.asyncio as redis

from handlers import bot_messages, user_commands, registration, handler_utils
from handlers.menu import phone_menu, settings_menu

from config_reader import config

from middlewares.anti_flood import AntiFloodMiddleware
from middlewares.check_reg import CheckRegistrationMiddleware

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB

import logging

# Logger init
logger = logging.getLogger(__name__)


async def main():
    # Создаем экземпляр бота
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    # Logging config
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s %(module)s'
    )

    # Mongo db storage
    cluster = AsyncIOMotorClient(config.db_token.get_secret_value())
    db: MDB = cluster.cryptan_game

    # Redis storage
    redis_storage = redis.Redis.from_url(config.redis_url.get_secret_value())

    # Middlewares registration
    dp.message.middleware(AntiFloodMiddleware())
    dp.message.middleware(CheckRegistrationMiddleware())
    dp.callback_query.middleware(CheckRegistrationMiddleware())

    # Подгружаем роутеры из пакетов
    dp.include_routers(
        user_commands.router,
        registration.router,
        bot_messages.router,
        settings_menu.router,
        phone_menu.router,
        handler_utils.router
    )

    # Отключаем dpu вебхук чтоб не получать сообщения скопившиеся при остановке бота
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг чтоб получать апдейты в реальном времени без остановки
    await dp.start_polling(bot, db=db, storage=redis_storage)

    logger.info('Bot started')


if __name__ == '__main__':
    asyncio.run(main())


# TODO: Сделать хендлер ошибок message cant be edited (высылать новое сообщение)
# Сделать если сообщение не последнее высылать новое
# Сделать бизнесы

# redis setup:
# sudo service redis-server restart, redis-cli
