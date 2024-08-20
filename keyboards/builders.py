from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import List


def inline_builder(
    text: str | List[str],
    callback_data: str | List[str],
    sizes: int | List[int] = 2,
    **kwargs
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    text = [text] if isinstance(text, str) else text
    callback_data = [callback_data] if isinstance(
        callback_data, str) else callback_data
    sizes = [sizes] if isinstance(sizes, int) else sizes

    [
        builder.button(text=txt, callback_data=cb)
        for txt, cb in zip(text, callback_data)
    ]

    builder.adjust(*sizes)
    return builder.as_markup(**kwargs)

def reply_builder(text: str | List[str]):
    builder = ReplyKeyboardBuilder()

    text = [text] if isinstance(text, str) else text

    [builder.button(text=el) for el in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
