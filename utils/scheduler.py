from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import json
import sqlite3
import logging

logger = logging.getLogger(__name__)

def is_sunday():
    result = datetime.now().weekday() == 6
    logger.debug(f"Is Sunday: {result}")
    return result

def load_schedule():
    logger.debug("Loading schedule from file")
    with open('schedule.json', 'r', encoding='utf-8') as f:
        schedule = json.load(f)
    logger.debug("Schedule loaded successfully")
    return schedule

def is_odd_week():
    result = datetime.now().isocalendar()[1] % 2 == 0
    logger.debug(f"Is odd week: {result}")
    return result

def get_db_connection():
    logger.debug("Establishing database connection")
    conn = sqlite3.connect('bot_database.db')
    conn.row_factory = sqlite3.Row
    logger.debug("Database connection established")
    return conn

def init_db():
    logger.info("Initializing database")
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                        (user_id INTEGER PRIMARY KEY, 
                        notifications_enabled INTEGER DEFAULT 1)''')
    logger.info("Database initialized")

def get_active_users():
    logger.debug("Fetching active users")
    with get_db_connection() as conn:
        users = conn.execute('SELECT user_id FROM users WHERE notifications_enabled = 1').fetchall()
    logger.debug(f"Found {len(users)} active users")
    return users

def get_current_schedule():
    logger.debug("Getting current schedule")
    schedule = load_schedule()
    week_type = "odd_week" if is_odd_week() else "even_week"
    today = datetime.now().strftime("%A").lower()
    current_schedule = schedule['groups'][0]['schedule'][week_type][today]
    logger.debug(f"Current schedule retrieved for {week_type}, {today}")
    return current_schedule

async def send_notification(bot: Bot, message: str):
    logger.info(f"Preparing to send notification: {message}")
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отключить уведомления", callback_data="disable_notifications")]])
    users = get_active_users()
    for user in users:
        try:
            await bot.send_message(user['user_id'], message, reply_markup=kb)
            logger.debug(f"Notification sent to user {user['user_id']}")
        except Exception as e:
            logger.error(f"Failed to send notification to user {user['user_id']}: {str(e)}")
    logger.info(f"Notification sending completed")

async def send_lesson_reminder(bot: Bot):
    logger.debug("Checking conditions for sending lesson reminder")
    if is_sunday() or not (datetime.strptime("08:00", "%H:%M").time() <= datetime.now().time() <= datetime.strptime("21:00", "%H:%M").time()):
        logger.debug("Conditions not met for sending lesson reminder")
        return

    now = datetime.now()
    logger.debug(f"Current time: {now}")
    for lesson in get_current_schedule():
        start_time = datetime.strptime(lesson['time'], "%H-%M").replace(year=now.year, month=now.month, day=now.day)
        end_time = start_time + timedelta(minutes=90)

        time_until_start = (start_time - now).total_seconds() / 60
        time_until_end = (end_time - now).total_seconds() / 60

        logger.debug(f"Lesson: {lesson['subject']}, Start time: {start_time}, End time: {end_time}")
        logger.debug(f"Time until start: {time_until_start} minutes, Time until end: {time_until_end} minutes")

        if 4 < time_until_start <= 5:
            message = f"🕒 Через 5 минут начнется пара: {lesson['subject']} ({lesson['type']}) в аудитории {lesson['room']}"
            logger.info(f"Sending start reminder for lesson: {lesson['subject']}")
            await send_notification(bot, message)

        elif 4 < time_until_end <= 5:
            message = f"🕒 Через 5 минут закончится пара: {lesson['subject']} ({lesson['type']}) в аудитории {lesson['room']}"
            logger.info(f"Sending end reminder for lesson: {lesson['subject']}")
            await send_notification(bot, message)


def schedule_daily_tasks(scheduler, bot):
    logger.info("Scheduling daily tasks")
    scheduler.add_job(send_lesson_reminder, 'cron', day_of_week='mon-sat', hour='8-21', minute='*/1', args=[bot])
    logger.info("Daily tasks scheduled")

# TODO: if lesson first, then send notification