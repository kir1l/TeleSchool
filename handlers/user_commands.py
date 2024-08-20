"""
Этот модуль обрабатывает основные команды пользователей в главном меню, включая команды "start" и "menu".

Команда "start": Отображает изображение с подписью и кнопку для перехода в главное меню.

Команда "menu": Отображает информацию о пользователе (имя, деньги, город) вместе со случайным изображением меню и клавиатурой главного меню.
"""

from aiogram import Router, F
from aiogram.filters import Command

from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto

from keyboards.builders import inline_builder
from keyboards.inline import menu_kb
from utils.player import get_player, Player

from motor.core import AgnosticDatabase as MDB
from aiogram.fsm.storage.redis import RedisStorage

from random import randint

router = Router()


# Обработчик на команду start
@router.message(Command('start'))
@router.callback_query(F.data == 'restart')
async def start_command(message: Message | CallbackQuery) -> None:
    print('start')

    photo_path = 'assets/photo/menu_3.jpg'
    response = dict(
        photo=FSInputFile(photo_path),
        caption='The bot has been successfully reloaded. Go to the main menu?',
        reply_markup=inline_builder('Main menu', 'menu', 1)
    )

    if isinstance(message, Message):
        await message.answer_photo(**response)  # If message
    else:
        await message.message.answer_photo(**response)  # If callback


@router.callback_query(F.data == 'menu')
async def menu_command(callback: CallbackQuery, storage: RedisStorage) -> None:
    print('menu')

    player: Player = get_player()

    user_name = await player.get_name()
    user_money = await player.get_money()
    user_city = await player.get_city()

    menu_photo_path = f'assets/photo/menu_{randint(1, 4)}.jpg'

    media = InputMediaPhoto(
        media=FSInputFile(menu_photo_path),
        caption=f'''Wassup, {user_name.title()}!\nYou are in {user_city.title()}. You have {user_money}$ on your Ledger''',
    )

    # if callback
    await callback.message.edit_media(media=media, reply_markup=menu_kb)
