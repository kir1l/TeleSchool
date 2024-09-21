from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Указать группу'),
            KeyboardButton(text='Мои занятия')
        ],
        [
            KeyboardButton(text='Настройки'),
            KeyboardButton(text='Искать по группе')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

