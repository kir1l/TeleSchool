# Сервис для расписания занятий - TeleSchool

Этот Telegram бот предоставляет удобный доступ к расписанию занятий для студентов. Он позволяет просматривать расписание на текущий день, на завтра, на всю неделю, а также получать информацию о текущем и следующем занятии.

## Функциональность

- Расписание на неделю
- Расписание на сегодня
- Расписание на завтра
- Информация о текущем занятии
- Информация о следующем занятии
- Настройки уведомлений

## Технологии

- aiogram 3.x
- SQLite
- APScheduler

## Установка и запуск

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Создайте файл `.env` в корневой директории проекта и добавьте в него токен вашего бота:

```python
BOT_TOKEN=your_bot_token_here
```
4. Запустите бота: `python main.py`

## Структура проекта

- `main.py`: Основной файл для запуска бота
- `config_reader.py`: Конфигурация и чтение переменных окружения
- `handlers/`: Обработчики команд пользователя
- `utils/`: Вспомогательные функции и утилиты
- `schedule.json`: Файл с расписанием занятий

## Разработка

Для добавления новых функций или изменения существующих, обратите внимание на следующие файлы:

- `handlers/user_commands.py`: Обработчики команд пользователя
- `utils/scheduler_utils.py`: Функции для работы с расписанием
- `utils/scheduler.py`: Настройка планировщика задач

## Лицензия

MIT
