from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Work 💸', callback_data='work'),
            InlineKeyboardButton(text='Phone 📱', callback_data='phone')
        ],
        [
            InlineKeyboardButton(text='🔄', callback_data='restart'),
            InlineKeyboardButton(text='City 🏙️', callback_data='current_city'),
            InlineKeyboardButton(text='⚙️', callback_data='settings')
        ]
    ]
)

settings_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Change name',
                                 callback_data='settings_change_nick'),
            InlineKeyboardButton(
                text='Skin color', callback_data='settings_change_skin'),
        ],
        [
            InlineKeyboardButton(text='Change gender',
                                 callback_data='settings_change_sex'),
            InlineKeyboardButton(text='Back', callback_data='menu'),
        ]
    ]
)

phone_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Business 💼', callback_data='business'),
            InlineKeyboardButton(text='Map 🌎', callback_data='map')
        ],
        [
            InlineKeyboardButton(text='Tasks 📋', callback_data='tasks'),
            InlineKeyboardButton(text='Profile 🙎🏻‍♂️', callback_data='profile')
        ],
        [
            InlineKeyboardButton(text='Back 🔙', callback_data='menu'),
        ]
    ]
)

work_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Scam', callback_data='work_scam'),
            InlineKeyboardButton(
                text='Arbitrage', callback_data='work_arbitrage')
        ],
        [
            InlineKeyboardButton(text='Back 🔙', callback_data='menu'),
        ]
    ]
)
