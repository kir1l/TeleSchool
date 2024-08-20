from aiogram import Router, F
from aiogram.types import FSInputFile, CallbackQuery, InputMediaPhoto, Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import settings_kb
from keyboards.builders import inline_builder

from motor.core import AgnosticDatabase as MDB

from utils.states import SettingsStates

router = Router()


# Меню настроек
@router.callback_query(F.data == 'settings')
async def open_settings(callback: CallbackQuery, state: FSMContext):
    settings_photo_path = 'assets/photo/settings.png'
    media = InputMediaPhoto(media=FSInputFile(
        settings_photo_path), caption='User settings ⚙️')

    await callback.message.edit_media(
        media=media,
        reply_markup=settings_kb
    )


# Смена имени
@router.callback_query(F.data == 'settings_change_nick')
async def settings_changeName(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.change_name)

    change_name_photo_path = 'assets/photo/registration_name.jpg'
    media = InputMediaPhoto(media=FSInputFile(change_name_photo_path),
                            caption='Write down new name:')
    await callback.message.edit_media(
        media=media
    )


@router.message(SettingsStates.change_name)
async def handle_new_name(message: Message, state: FSMContext, db: MDB):
    new_name = message.text
    await db.users.update_one({'_id': message.from_user.id}, {'$set': {'name': new_name}})
    await state.clear()  # Сбрасываем состояние

    change_name_photo_path = FSInputFile('assets/photo/menu_3.jpg')
    await message.answer_photo(photo=change_name_photo_path, caption=f'Your new name: {new_name}', reply_markup=settings_kb)


# Изменение пола
@router.callback_query(F.data == 'settings_change_sex')
async def settings_changeSex(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.change_sex)

    change_sex_photo_path = 'assets/photo/choose_sex.jpg'
    media = InputMediaPhoto(media=FSInputFile(change_sex_photo_path),
                            caption='Choose gender:')

    await callback.message.edit_media(
        media=media,
        reply_markup=inline_builder(
            ['Male', 'Female'],
            ['male', 'female']
        )
    )


@router.callback_query(SettingsStates.change_sex)
async def handle_new_sex(callback: CallbackQuery, state: FSMContext, db: MDB):
    new_sex = callback.data

    await db.users.update_one({'_id': callback.from_user.id}, {'$set': {'sex': new_sex}})
    await state.clear()  # Сбрасываем состояние

    change_sex_photo_path = 'assets/photo/menu_3.jpg'
    media = InputMediaPhoto(media=FSInputFile(
        change_sex_photo_path), caption=f'Gender changed successfully')

    await callback.message.edit_media(media=media, reply_markup=settings_kb)


# Изменение цвета кожи
@router.callback_query(F.data == 'settings_change_skin')
async def settings_changeSkin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.change_skinColor)

    change_skin_photo_path = 'assets/photo/choose_skin.jpg'
    media = InputMediaPhoto(media=FSInputFile(
        change_skin_photo_path), caption='Choose new skin color:')

    await callback.message.edit_media(
        media=media,
        reply_markup=inline_builder(
            ['White', 'Black'],
            ['white', 'black']
        )
    )


@router.callback_query(SettingsStates.change_skinColor)
async def handle_new_skin(callback: CallbackQuery, state: FSMContext, db: MDB):
    new_skin = callback.data

    await db.users.update_one({'_id': callback.from_user.id}, {'$set': {'skin_color': new_skin}})
    await state.clear()  # Сбрасываем состояние

    change_skin_photo_path = 'assets/photo/menu_3.jpg'
    media = InputMediaPhoto(media=FSInputFile(
        change_skin_photo_path), caption=f'Skin color changed successfully')

    await callback.message.edit_media(media=media, reply_markup=settings_kb)
