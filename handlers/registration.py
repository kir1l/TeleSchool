from aiogram import Router, F
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from utils.states import Reg_form, registration_state
from utils.player import Player
from keyboards.builders import inline_builder

from motor.core import AgnosticDatabase as MDB

router = Router()


@router.callback_query(F.data == "start_registration")
async def registration(callback: CallbackQuery, state: FSMContext, db: MDB, storage: RedisStorage):
    user_id = await storage.get(f"player:{callback.from_user.id}:name")

    # Если пользователь уже зарегистрирован
    if user_id:
        await callback.message.answer("You already registered.", reply_markup=inline_builder('Main menu', 'menu', 1))
        return

    # Измените состояние на ожидание имени
    await state.set_state(Reg_form.name)

    photo_path = 'assets/photo/registration_name.jpg'
    media = InputMediaPhoto(
        media=FSInputFile(photo_path),
        caption='Lets start, write down what you want me to call you'
    )

    await callback.message.edit_media(media=media)


@router.message(Reg_form.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохраняем имя пользователя
    await state.set_state(Reg_form.sex)  # Переход к состоянию выбора пола

    # Отправляем сообщение с выбором пола
    photo_path = 'assets/photo/choose_sex.jpg'  # Путь к фотографии выбора пола
    message_with_sex_selection = await message.answer_photo(
        photo=FSInputFile(photo_path),
        caption='Great! Now lets choose gender:',
        reply_markup=inline_builder(
            ['Male', 'Female'],
            ['male', 'female']
        )
    )

    # Сохраняем ID сообщения для дальнейшего редактирования
    await state.update_data(message_id=message_with_sex_selection.message_id)


@router.callback_query(Reg_form.sex)
async def registration_sex(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex=callback.data)  # Сохраняем пол
    # Переход к состоянию выбора цвета
    await state.set_state(Reg_form.skinColor)

    data = await state.get_data()

    photo_path = 'assets/photo/choose_skin.jpg'  # Путь к фото выбора цвета

    media = InputMediaPhoto(
        media=FSInputFile(photo_path),
        caption='Chose your skin color:'
    )

    await callback.message.edit_media(
        media=media,
        reply_markup=inline_builder(
            ['White', 'Black'],
            ['white', 'black']
        )
    )


@router.callback_query(Reg_form.skinColor)
async def registration_end(callback: CallbackQuery, state: FSMContext, db: MDB, storage: RedisStorage):
    await state.update_data(skin_color=callback.data)  # Сохраняем цвет кожи
    data = await state.get_data()  # Получаем все данные из состояния

    # Переменная состояния регистрации, при true CheckReg не работает
    global registration_state

    # Создаем экземпляр Player
    player = Player(
        id=callback.from_user.id,
        name=data['name'],
        money=0,  # Начальное количество денег
        sex=data['sex'],
        skin_color=data['skin_color'],
        db=db,
        redis_storage=storage  # Передаем RedisStorage
    )

    # Сохраняем данные в БД и кешируем
    await player.save_data()
    await player.cache_data()

    # Даем стартовые 5000$
    player.add_money(5000)

    media = InputMediaPhoto(
        media=FSInputFile('assets/photo/menu_3.jpg'),
        caption='Registration completed! +5000$'
    )

    print('Переводим стейт регистрации в завершенный')
    # По завершению переводим состояние регистрации в False
    registration_state = False

    await callback.message.edit_media(
        media=media,
        reply_markup=inline_builder('Main menu', 'menu')
    )

    await state.clear()  # Очищаем состояние


@router.message(Reg_form.sex)
@router.message(Reg_form.skinColor)
async def incorrect_registration_sex(message: Message):
    await message.answer('Use buttons!')
