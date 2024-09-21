from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.scheduler_utils import get_weekly_schedule, get_today_schedule, get_current_lesson, get_next_lesson, get_tomorrow_schedule
from utils.scheduler import get_db_connection

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    with get_db_connection() as conn:
        conn.execute('INSERT or IGNORE INTO users (user_id, notifications_enabled) VALUES (?, 1)', (user_id,))

    kb = [
        [types.KeyboardButton(text="Расписание на неделю")],
        [types.KeyboardButton(text="Расписание на сегодня")],
        [types.KeyboardButton(text="Расписание на завтра")],
        [types.KeyboardButton(text="Текущее занятие")],
        [types.KeyboardButton(text="Следующее занятие")],
        [types.KeyboardButton(text="Настройки")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите действие:", reply_markup=keyboard)

@router.message(F.text == "Расписание на неделю")
async def weekly_schedule(message: types.Message):
    await message.answer(get_weekly_schedule())

@router.message(F.text == "Расписание на сегодня")
async def today_schedule(message: types.Message):
    await message.answer(get_today_schedule())

@router.message(F.text == "Расписание на завтра")
async def tomorrow_schedule(message: types.Message):
    schedule = get_tomorrow_schedule()
    await message.answer(schedule)

@router.message(F.text == "Текущее занятие")
async def current_lesson(message: types.Message):
    await message.answer(get_current_lesson())

@router.message(F.text == "Следующее занятие")
async def next_lesson(message: types.Message):
    await message.answer(get_next_lesson())

@router.message(F.text == "Настройки")
async def open_settings(message: types.Message):
    with get_db_connection() as conn:
        user = conn.execute('SELECT notifications_enabled FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()

    status = "включены ✅" if user['notifications_enabled'] else "выключены ❌"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{'Выключить' if user['notifications_enabled'] else 'Включить'} уведомления", 
                              callback_data=f"toggle_notifications_{0 if user['notifications_enabled'] else 1}")]
    ])
    await message.answer(f"⚙️ Настройки\n\nУведомления сейчас {status}", reply_markup=kb)

@router.callback_query(F.data.startswith("toggle_notifications_"))
async def toggle_notifications(callback: types.CallbackQuery):
    new_status = int(callback.data.split("_")[-1])
    with get_db_connection() as conn:
        conn.execute('UPDATE users SET notifications_enabled = ? WHERE user_id = ?', (new_status, callback.from_user.id))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{'Выключить' if new_status == 1 else 'Включить'} уведомления", 
                              callback_data=f"toggle_notifications_{0 if new_status == 1 else 1}")]
    ])

    await callback.answer("Настройки уведомлений обновлены")
    await callback.message.edit_text(f"⚙️ Настройки\n\nУведомления {'включены ✅' if new_status == 1 else 'выключены ❌'}", reply_markup=kb)

@router.callback_query(F.data == 'disable_notifications')
async def disable_notifications(callback: types.CallbackQuery):
    with get_db_connection() as conn:
        conn.execute('UPDATE users SET notifications_enabled = 0 WHERE user_id = ?', (callback.from_user.id,))
    await callback.answer("Уведомления отключены ❌")