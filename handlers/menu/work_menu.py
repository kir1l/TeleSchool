from aiogram import Router, F
from aiogram.types import FSInputFile, CallbackQuery, InputMediaPhoto, Message

from keyboards.inline import settings_kb

from motor.core import AgnosticDatabase as MDB

from utils.player import get_player

router = Router()


# Меню работы
@router.callback_query(F.data == 'work')
async def open_settings(callback: CallbackQuery) -> None:
    settings_photo_path = 'assets/photo/work.png'
    media = InputMediaPhoto(media=FSInputFile(
        settings_photo_path), caption='Here you can earn money by completing different tasks:')

    await callback.message.edit_media(
        media=media,
        reply_markup=settings_kb
    )

# Меню скама (реферальная программа)


@router.callback_query(F.data == 'work')
async def open_settings(callback: CallbackQuery) -> None:

    player = get_player()

    settings_photo_path = 'assets/photo/work.png'
    media = InputMediaPhoto(media=FSInputFile(
        settings_photo_path), caption='Here you can earn money by completing different tasks:')

    await callback.message.edit_media(
        media=media,
        reply_markup=settings_kb
    )
