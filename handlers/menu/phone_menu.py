from aiogram import Router, F
from aiogram.types import FSInputFile, CallbackQuery, InputMediaPhoto, Message

from keyboards.inline import phone_kb
from keyboards.builders import inline_builder

from motor.core import AgnosticDatabase as MDB

from utils.states import SettingsStates

router = Router()


# Меню телефона
@router.callback_query(F.data == 'phone')
async def open_phone(callback: CallbackQuery):
    settings_photo_path = 'assets/photo/phone.jpg'
    media = InputMediaPhoto(media=FSInputFile(settings_photo_path),
                            caption='Choose app 📱')
    await callback.message.edit_media(
        media=media,
        reply_markup=phone_kb
    )


# Меню карты
@router.message(F.data == 'map')
async def handle_new_name(message: Message, db: MDB):

    change_name_photo_path = 'assets/photo/menu_3.jpg'
    media = InputMediaPhoto(media=FSInputFile(
        change_name_photo_path), caption=f'Имя успешно изменено на')
   #  await message.edit_media(media=media, reply_markup=settings_kb)
