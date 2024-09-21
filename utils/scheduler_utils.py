import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

DAYS_TRANSLATION = {
    'monday': 'Понедельник',
    'tuesday': 'Вторник',
    'wednesday': 'Среда',
    'thursday': 'Четверг',
    'friday': 'Пятница',
    'saturday': 'Суббота',
    'sunday': 'Воскресенье'
}

def format_time(minutes):
    logger.debug(f"Formatting time for {minutes} minutes")
    hours, mins = divmod(minutes, 60)
    
    if hours > 0:
        hour_str = f"{hours} час" if hours == 1 else f"{hours} часа" if 2 <= hours <= 4 else f"{hours} часов"
        if mins > 0:
            min_str = get_minute_string(mins)
            return f"{hour_str} {min_str}"
        return hour_str
    else:
        return get_minute_string(mins)

def get_minute_string(mins):
    logger.debug(f"Getting minute string for {mins} minutes")
    if mins % 10 == 1 and mins % 100 != 11:
        return f"{mins} минута"
    elif 2 <= mins % 10 <= 4 and (mins % 100 < 10 or mins % 100 >= 20):
        return f"{mins} минуты"
    else:
        return f"{mins} минут"

def is_sunday(date=None):
    date = date or datetime.now()
    logger.debug(f"Checking if {date} is Sunday")
    return date.weekday() == 6

def load_schedule():
    logger.info("Loading schedule from file")
    with open('schedule.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def is_odd_week(date=None):
    date = date or datetime.now()
    logger.debug(f"Checking if {date} is in an odd week")
    return date.isocalendar()[1] % 2 == 0

def get_week_type(date=None):
    logger.debug(f"Getting week type for {date}")
    return "odd_week" if is_odd_week(date) else "even_week"

def get_weekly_schedule():
    logger.info("Generating weekly schedule")
    schedule = load_schedule()
    week_type = get_week_type()
    result = f"📅 Расписание на {'нечетную' if is_odd_week() else 'четную'} неделю:\n\n"
    
    for day, lessons in schedule['groups'][0]['schedule'][week_type].items():
        result += format_day_schedule(day, lessons)
    
    logger.info("Generated weekly schedule")
    return result

def get_today_schedule():
    logger.info("Getting today's schedule")
    return get_day_schedule(datetime.now())

def get_tomorrow_schedule():
    logger.info("Getting tomorrow's schedule")
    return get_day_schedule(datetime.now() + timedelta(days=1))

def get_day_schedule(date):
    logger.info(f"Getting schedule for {date}")
    schedule = load_schedule()
    week_type = get_week_type(date)
    day = date.strftime("%A").lower()

    if is_sunday(date):
        logger.info("No classes on Sunday")
        return f"{'Сегодня' if date.date() == datetime.now().date() else 'Завтра'} выходной день. Занятий нет."
    
    result = f"📅 Расписание на {'сегодня' if date.date() == datetime.now().date() else 'завтра'} ({DAYS_TRANSLATION[day]}):\n\n"
    result += format_lessons(schedule['groups'][0]['schedule'][week_type][day])
    
    logger.info(f"Generated schedule for {date.strftime('%Y-%m-%d')}")
    return result

def get_current_lesson():
    logger.info("Getting current lesson")
    schedule = load_schedule()
    week_type = get_week_type()
    today = datetime.now().strftime("%A").lower()
    current_time = datetime.now().time()
    
    for lesson in schedule['groups'][0]['schedule'][week_type][today]:
        start_time, end_time = get_lesson_times(lesson['time'])
        
        if start_time <= current_time <= end_time:
            remaining_time = datetime.combine(datetime.today(), end_time) - datetime.now()
            minutes_left = remaining_time.seconds // 60
            logger.info(f"Current lesson: {lesson['subject']}")
            return format_current_lesson(lesson, minutes_left)
        
        if current_time < start_time:
            time_until_start = datetime.combine(datetime.today(), start_time) - datetime.now()
            minutes_until_start = time_until_start.seconds // 60
            logger.info(f"Next lesson: {lesson['subject']}")
            return format_next_lesson(lesson, minutes_until_start)
    
    logger.info("No more lessons for today")
    return "🕒 Занятия на сегодня окончены"

def get_next_lesson():
    logger.info("Getting next lesson")
    schedule = load_schedule()
    week_type = get_week_type()
    today = datetime.now().strftime("%A").lower()
    current_time = datetime.now().time()
    
    for lesson in schedule['groups'][0]['schedule'][week_type][today]:
        start_time = datetime.strptime(lesson['time'], "%H-%M").time()
        
        if current_time < start_time:
            time_until_start = datetime.combine(datetime.today(), start_time) - datetime.now()
            minutes_until_start = time_until_start.seconds // 60
            logger.info(f"Next lesson today: {lesson['subject']}")
            return format_next_lesson(lesson, minutes_until_start, include_time=True)
    
    logger.info("No more lessons today, checking next day")
    return get_next_day_lesson(schedule, week_type)

def format_day_schedule(day, lessons):
    logger.debug(f"Formatting schedule for {day}")
    result = f"🗓 {DAYS_TRANSLATION[day]}:\n"
    result += format_lessons(lessons)
    return result + "\n"

def format_lessons(lessons):
    logger.debug(f"Formatting {len(lessons)} lessons")
    return "".join([f"{i}. {lesson['time'].replace('-', ':')} - {lesson['subject']} ({lesson['type']}) - {lesson['room']}\n"
                    for i, lesson in enumerate(lessons, 1)])

def get_lesson_times(time_str):
    logger.debug(f"Getting lesson times for {time_str}")
    start_time = datetime.strptime(time_str, "%H-%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=90)).time()
    return start_time, end_time

def format_current_lesson(lesson, minutes_left):
    logger.debug(f"Formatting current lesson: {lesson['subject']}")
    return f"🕒 Текущая пара:\n{lesson['subject']} ({lesson['type']})\nАудитория: {lesson['room']}\nДо конца пары осталось {format_time(minutes_left)}"

def format_next_lesson(lesson, minutes_until_start, include_time=False):
    logger.debug(f"Formatting next lesson: {lesson['subject']}")
    time_info = f"Начало в {lesson['time'].replace('-', ':')}\n" if include_time else ""
    return f"🕒 Следующая пара:\n{lesson['subject']} ({lesson['type']})\nАудитория: {lesson['room']}\n{time_info}До начала занятия осталось: {format_time(minutes_until_start)}"

def get_next_day_lesson(schedule, week_type):
    logger.info("Getting next day's lesson")
    next_day = (datetime.now() + timedelta(days=1)).strftime("%A").lower()
    if next_day in schedule['groups'][0]['schedule'][week_type]:
        next_lesson = schedule['groups'][0]['schedule'][week_type][next_day][0]
        logger.info(f"Next day's lesson: {next_lesson['subject']}")
        return f"🕒 Следующая пара завтра ({DAYS_TRANSLATION[next_day]}):\n{next_lesson['subject']} ({next_lesson['type']})\nАудитория: {next_lesson['room']}\nНачало в {next_lesson['time'].replace('-', ':')}"
    logger.info("No lessons scheduled for the near future")
    return "На ближайшее время занятий не запланировано"