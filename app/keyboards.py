# Year keyboard
import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Year keyboard
def create_year_keyboard():
    current_year = datetime.now().year
    years = [str(y) for y in range(current_year, current_year + 10)]
    year_buttons = [InlineKeyboardButton(year, callback_data=f"set_year|{year}") for year in years]
    year_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=3)
    year_keyboard.add(*year_buttons)
    year_keyboard.row(back_button, cancel_button, next_button)

    return year_keyboard


# Month keyboard
def create_month_keyboard():
    month_buttons = [InlineKeyboardButton(calendar.month_abbr[i], callback_data=f"set_month|{i}") for i in range(1, 13)]
    month_keyboard = InlineKeyboardMarkup(row_width=3)
    month_keyboard.add(*month_buttons)
    month_keyboard.row(back_button, cancel_button, next_button)
    return month_keyboard


# Weekday keyboard
def create_weekday_keyboard():
    week_buttons = [InlineKeyboardButton(calendar.day_abbr[i], callback_data=f'set_weekday|{i}') for i in range(1, 8)]
    week_keyboard = InlineKeyboardMarkup(row_width=3)
    week_keyboard.add(*week_buttons)
    week_keyboard.row(back_button, cancel_button, next_button)
    return week_keyboard


# Day keyboard
def create_day_keyboard(year, month):
    number_of_days = calendar.monthrange(year, month)[1]
    print(year, month, number_of_days)
    day_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_day|{i}") for i in range(1, number_of_days + 1)]
    day_keyboard = InlineKeyboardMarkup(row_width=3)
    day_keyboard.add(*day_buttons)
    day_keyboard.row(back_button, cancel_button, next_button)
    return day_keyboard


# Hour keyboard
def create_hour_keyboard():
    ampm_buttons = [InlineKeyboardButton("AM", callback_data="set_ampm|am"),
                    InlineKeyboardButton("PM", callback_data="set_ampm|pm"), ]
    hour_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_hour|{i}") for i in range(1, 13)]
    hour_keyboard = InlineKeyboardMarkup(row_width=3)
    hour_keyboard.row(*ampm_buttons)
    hour_keyboard.add(*hour_buttons)
    hour_keyboard.row(back_button, cancel_button, next_button)
    return hour_keyboard


# Minute keyboard
def create_minute_keyboard():
    minute_buttons = []

    for minute in range(0, 60, 5):
        new_min = minute
        if len(str(minute)) == 1:
            new_min = '0' + str(minute)

        minute_buttons.append(InlineKeyboardButton(str(new_min), callback_data=f"set_minute|{new_min}"))

    minute_keyboard = InlineKeyboardMarkup(row_width=3)
    minute_keyboard.add(*minute_buttons)
    minute_keyboard.row(back_button, cancel_button, next_button)
    return minute_keyboard


def create_keyboard_according_date_type(date_type: str, date_data: dict = None):

    match date_type:
        case 'year':
            return create_year_keyboard()
        case 'month':
            return create_month_keyboard()
        case 'week':
            return create_weekday_keyboard()
        case 'day':
            return create_day_keyboard(int(date_data.get('year')), int(date_data.get('month')))
        case 'hour':
            return create_hour_keyboard()
        case 'ampm':
            return create_hour_keyboard()
        case 'minute':
            return create_minute_keyboard()


# Back, Cancel, and Next buttons with their proxies
back_button = InlineKeyboardButton('◀️Back', callback_data="date_back")
cancel_button = InlineKeyboardButton('Cancel', callback_data="date_cancel")
next_button = InlineKeyboardButton('Next▶️', callback_data="date_next")


# Task keyboards
one_time_task_button = InlineKeyboardButton("One time task", callback_data="one_time_task")
routine_task_button = InlineKeyboardButton("Routine task", callback_data="routine_task")
close_button = InlineKeyboardButton("Close", callback_data="close")

task_inline_keyboard = InlineKeyboardMarkup(row_width=2).add(
    one_time_task_button,
    routine_task_button,
    close_button,
)


# one time task meny
def create_one_time_task_menu_keyboard():
    one_time_task_menu_kb = InlineKeyboardMarkup(row_width=2)
    add_task_button = InlineKeyboardButton("Add Task", callback_data='add_one_time_task')
    see_all_button = InlineKeyboardButton("See All Task", callback_data='see_all_one_time_task')
    back_button_task = InlineKeyboardButton("Back", callback_data='back_one_time_task')
    one_time_task_menu_kb.add(add_task_button, see_all_button, back_button_task)
    return one_time_task_menu_kb
# one time task modification keyboard


def create_one_time_task_create_task_parameters():
    task_parameters_kb = InlineKeyboardMarkup(row_width=1)
    task_name_button = InlineKeyboardButton(text="Name 🏷️", callback_data="set_name")
    start_date_button = InlineKeyboardButton(text="Start Date 📅", callback_data="set_start_date")
    due_date_button = InlineKeyboardButton(text="Due Date 📅", callback_data="set_due_date")
    description_button = InlineKeyboardButton(text="Description ✏️", callback_data="set_description")
    status_button = InlineKeyboardButton(text="Status ✅", callback_data="set_status")
    delete_button = InlineKeyboardButton(text="Delete ❌", callback_data="delete_task")
    task_parameters_kb.add(task_name_button)
    task_parameters_kb.row(start_date_button, due_date_button)
    task_parameters_kb.add(description_button, status_button, delete_button)
    return task_parameters_kb
