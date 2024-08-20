import aiogram.fsm.storage.redis
from typing import Dict, Any

from motor.core import AgnosticDatabase as MDB
from aiogram.fsm.storage.redis import RedisStorage

player = None


class Player:
    def __init__(self, id: int, name: str, money: int, sex: str, skin_color: str, db: MDB, redis_storage):
        self._id: int = id
        self._name: str = name | f'Player {self._id}'
        self._money: int = money | 0
        self._sex: str = sex | 'male'
        self._skin_color: str = skin_color | 'white'

        # Defaults
        self._current_city: str = 'moscow'
        self._scam_level: int = 0
        self._inventory: dict = {}
        self._squad_id: int = 0
        self._referrals: int = 0

        # Utils
        self.db: MDB = db  # Добавление ссылки на коллекцию MongoDB
        self.redis_storage = redis_storage  # Добавление ссылки на Redis

    async def set_name(self, new_name: str) -> None:
        self._name = new_name
        await self.db.users.update_one({"_id": self._id}, {"$set": {"name": self._name}})
        await self.redis_storage.set(f"player:{self._id}:name", self._name)

    async def get_name(self) -> str:
        redis_name = await self.redis_storage.get(f"player:{self._id}:name")
        if redis_name is not None:
            return redis_name.decode('utf-8')  # Декодируем байты в строку

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["name"]

        return self._name

    async def subtract_money(self, value: int) -> None:
        self._money -= value
        await self.db.users.update_one({"_id": self._id}, {"$set": {"money": self._money}})
        await self.redis_storage.set(f"player:{self._id}:money", self._money)

    async def add_money(self, value: int) -> None:
        self._money += value
        await self.db.users.update_one({"_id": self._id}, {"$set": {"money": self._money}})
        await self.redis_storage.set(f"player:{self._id}:money", self._money)

    async def get_money(self) -> int:
        redis_money = await self.redis_storage.get(f"player:{self._id}:money")
        if redis_money is not None:
            return int(redis_money)

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["money"]

        return self._money

    async def set_squad_id(self, id: int) -> None:
        self._squad_id = id
        await self.db.users.update_one({"_id": self._id}, {"$set": {"squad_id": self._squad_id}})
        await self.redis_storage.set(f"player:{self._id}:squad_id", self._squad_id)

    async def get_squad_id(self) -> int:
        redis_squad_id = await self.redis_storage.get(f"player:{self._id}:squad_id")
        if redis_squad_id is not None:
            return int(redis_squad_id)

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["squad_id"]

        return self._squad_id

    async def has_squad(self) -> bool:
        return self._squad_id != 0

    async def set_city(self, new_city: str) -> None:
        cities = ['Moscow', 'Las Vegas', 'Dubai', 'Hong Kong']
        if new_city in cities:
            self._current_city = new_city
            await self.db.users.update_one({"_id": self._id}, {"$set": {"current_city": self._current_city}})
            await self.redis_storage.set(f"player:{self._id}:current_city", self._current_city)
        else:
            print('Incorrect city name')

    async def get_city(self) -> str:
        redis_city = await self.redis_storage.get(f"player:{self._id}:current_city")
        if redis_city is not None:
            return redis_city.decode('utf-8')

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["current_city"]

        return self._current_city

    async def set_sex(self, new_sex: str) -> None:
        self._sex = new_sex
        await self.db.users.update_one({"_id": self._id}, {"$set": {"sex": self._sex}})
        await self.redis_storage.set(f"player:{self._id}:sex", self._sex)

    async def get_sex(self) -> str:
        redis_sex = await self.redis_storage.get(f"player:{self._id}:sex")
        if redis_sex is not None:
            return redis_sex.decode('utf-8')

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["sex"]

        return self._sex

    async def set_skin_color(self, new_color: str) -> None:
        self._skin_color = new_color
        await self.db.users.update_one({"_id": self._id}, {"$set": {"skin_color": self._skin_color}})
        await self.redis_storage.set(f"player:{self._id}:skin_color", self._skin_color)

    async def get_skin_color(self) -> str:
        redis_skin_color = await self.redis_storage.get(f"player:{self._id}:skin_color")
        if redis_skin_color is not None:
            return redis_skin_color.decode('utf-8')

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["skin_color"]

        return self._skin_color

    async def get_info(self) -> Dict[str, Any]:
        info = dict(
            _id=self._id,
            name=await self.get_name(),
            money=await self.get_money(),
            inventory=self._inventory,
            squad_id=await self.get_squad_id(),
            current_city=await self.get_city(),
            sex=await self.get_sex(),
            skin_color=await self.get_skin_color()
        )
        return info

    async def cache_data(self) -> None:
        print('кеширование данных')
        # Получаем данные о игроке из MongoDB
        mongo_data = await self.db.users.find_one({"_id": self._id})

        if mongo_data:
            # Словарь для соответствия полей
            fields = {
                "name": "_name",
                "money": "_money",
                "squad_id": "_squad_id",
                "current_city": "_current_city",
                "sex": "_sex",
                "skin_color": "_skin_color",
            }

            # Кешируем данные в Redis и обновляем локальные атрибуты
            for mongo_field, class_attr in fields.items():
                value = mongo_data.get(mongo_field, getattr(self, class_attr))
                await self.redis_storage.set(f"player:{self._id}:{mongo_field}", value)
                setattr(self, class_attr, value)
        else:
            # Если данных нет в MongoDB
            print(f"No data found for player with id {self._id}")

    async def save_data(self) -> None:
        print('сохранение данных в бд')
        # Создаем словарь для хранения данных игрока
        player_data = {
            "name": self._name,
            "money": self._money,
            "squad_id": self._squad_id,
            "current_city": self._current_city,
            "sex": self._sex,
            "skin_color": self._skin_color,
        }

        # Сохраняем данные в MongoDB
        await self.db.users.update_one({"_id": self._id}, {"$set": player_data}, upsert=True)

    async def add_scam_level(self, value: int) -> None:
        self._money += value
        await self.db.users.update_one({"_id": self._id}, {"$set": {"money": self._money}})
        await self.redis_storage.set(f"player:{self._id}:money", self._money)

    async def get_money(self) -> int:
        redis_money = await self.redis_storage.get(f"player:{self._id}:money")
        if redis_money is not None:
            return int(redis_money)

        mongo_data = await self.db.users.find_one({"_id": self._id})
        if mongo_data:
            return mongo_data["money"]

        return self._money


async def init_player_by_db(db: MDB, storage: RedisStorage, id=None, data=None) -> Player:
    print('Player init')

    if not id or data:
        print('No data or id')
        return

    if not data:
        data = await db.users.find_one({"_id": id})

        if not data:
            raise ValueError(f"Player with ID {id} not found")

        global player
        player = Player(
            id=data["_id"],
            name=data["name"],
            money=data["money"],
            sex=data["sex"],
            skin_color=data["skin_color"],
            db=db,
            redis_storage=storage
        )

        print('Cache data')
        await player.cache_data()

        return player


def get_player() -> Player:
    if not isinstance(player, Player):
        print('player is not initialized')
        return None

    return player
