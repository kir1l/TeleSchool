from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def use_buttons(message: Message):
    await message.answer('Use buttons!')
