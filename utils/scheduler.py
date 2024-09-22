from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.scheduler_utils import get_today_schedule, get_next_lesson, get_current_lesson, is_sunday, load_schedule, is_odd_week
from datetime import datetime, timedelta
from utils.database import db

async def send_lesson_reminder(bot: Bot):
    if is_sunday():
        return

    now = datetime.now()
    if now.time() < datetime.strptime("08:00", "%H:%M").time() or now.time() > datetime.strptime("21:00", "%H:%M").time():
        return

    users = db.get_active_users()
    schedule = load_schedule()
    week_type = "odd_week" if is_odd_week() else "even_week"
    today = now.strftime("%A").lower()

    for lesson in schedule['groups'][0]['schedule'][week_type][today]:
        start_time = datetime.strptime(lesson['time'].split('-')[0], "%H-%M").replace(year=now.year, month=now.month, day=now.day)
        end_time = start_time + timedelta(minutes=90)

        time_until_start = (start_time - now).total_seconds() / 60
        time_until_end = (end_time - now).total_seconds() / 60

        if 9 < time_until_start <= 10:
            message = f"Через 10 минут начнется пара: {lesson['subject']} ({lesson['type']}) в аудитории {lesson['room']}"
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отключить уведомления", callback_data="disable_notifications")]])
            for user in users:
                await bot.send_message(user['user_id'], message, reply_markup=kb)

        elif 9 < time_until_end <= 10:
            message = f"Через 10 минут закончится пара: {lesson['subject']} ({lesson['type']}) в аудитории {lesson['room']}"
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отключить уведомления", callback_data="disable_notifications")]])
            for user in users:
                await bot.send_message(user['user_id'], message, reply_markup=kb)

async def send_daily_schedule(bot: Bot):
    if is_sunday():
        return

    users = db.get_active_users()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A").lower()
    schedule = get_today_schedule(tomorrow)
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отключить уведомления", callback_data="disable_notifications")]])
    
    for user in users:
        await bot.send_message(user['user_id'], f"Расписание на завтра:\n{schedule}", reply_markup=kb)

def schedule_daily_tasks(scheduler, bot):
    scheduler.add_job(send_lesson_reminder, 'cron', day_of_week='mon-sat', hour='8-21', minute='*/5', args=[bot])
    scheduler.add_job(send_daily_schedule, 'cron', hour=22, minute=0, args=[bot])