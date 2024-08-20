"""
Класс `CheckRegistrationMiddleware` - это middleware, который проверяет регистрацию пользователя в базе данных приложения перед предоставлением доступа к функциональности бота.

Middleware выполняет следующие действия:

1. Проверяет глобальную переменную `registration_state` на True. Если она установлена в True, это означает, что пользователь в данный момент проходит регистрацию. В этом случае middleware разрешает обработчику сообщения продолжить работу.

2. Извлекает ID пользователя из входящего сообщения.

3. Проверяет наличие информации о пользователе в кэше Redis. Если информация найдена, middleware инициализирует объект `Player` для пользователя и разрешает обработчику сообщения продолжить работу.

4. Если информация о пользователе не найдена в Redis, middleware проверяет базу данных MongoDB на наличие данных пользователя. Если данные найдены, middleware инициализирует объект `Player` для пользователя, кэширует данные в Redis и разрешает обработчику сообщения продолжить работу.

5. Если пользователь не найден ни в Redis, ни в MongoDB, middleware отправляет пользователю запрос на регистрацию, включая фотографию и кнопку на inline клавиатуре для запуска процесса регистрации. Затем middleware устанавливает глобальную переменную `registration_state` в True, чтобы указать, что пользователь находится в процессе регистрации.
"""

from typing import Callable, Awaitable, Dict, Any
# Aiogram
from aiogram import BaseMiddleware
from aiogram.types import Message, FSInputFile
# Custom
from utils.player import Player, init_player_by_db, get_player
from keyboards.builders import inline_builder
from utils.states import registration_state
# DB
from aiogram.fsm.storage.redis import RedisStorage
from motor.core import AgnosticDatabase as MDB


class CheckRegistrationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        global registration_state

        # Возвращаем контроль хендлеру если стоит стейт регистрации
        if registration_state:
            return await handler(event, data)

        user_id = event.from_user.id  # Получаем ID пользователя из сообщения

        redis_storage: RedisStorage = data['storage']
        db: MDB = data['db']

        # Проверка на наличие юзера в Redis
        redis_name = await redis_storage.get(f"player:{user_id}:name")

        # Пользователь уже зарегистрирован в Redis
        if redis_name is not None:
            # Проверяем наличие экземпляра Player
            player = get_player()
            if not player:
                # Если пользователь не инициализирован, инициализируем
                await init_player_by_db(db=db, storage=redis_storage, id=user_id)

            return await handler(event, data)

        # Проверка на наличие в MongoDB, если не нашли в redis
        mongo_data = await db.users.find_one({"_id": user_id})
        if mongo_data:
            player = await init_player_by_db(db=db, storage=redis_storage, data=mongo_data)
            player.cache_data()

            return await handler(event, data)

        # Если пользователь не найден ни в Redis, ни в БД, предложим зарегистрироваться
        photo_path = 'assets/photo/registration.png'
        await event.answer_photo(
            photo=FSInputFile(photo_path),
            caption='Hi! I see you are not registered yet, so lets get started',
            reply_markup=inline_builder('Lets start', 'start_registration', 1)
        )

        # Переводим состояние регистрации в активное, при ней мидлварь не работает
        registration_state = True
        return  # Завершаем выполнение middleware
