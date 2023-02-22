# Year keyboard
import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Year keyboard
current_year = datetime.now().year
years = [str(y) for y in range(current_year, current_year + 10)]
year_buttons = [InlineKeyboardButton(year, callback_data=f"set_year|{year}") for year in years]
year_keyboard = InlineKeyboardMarkup(row_width=3)
year_keyboard.add(*year_buttons)

# Month keyboard
month_buttons = [InlineKeyboardButton(calendar.month_abbr[i], callback_data=f"set_month|{i}") for i in range(1, 13)]
month_keyboard = InlineKeyboardMarkup(row_width=3)
month_keyboard.add(*month_buttons)

# Day keyboard
day_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_day|{i}") for i in range(1, 32)]
day_keyboard = InlineKeyboardMarkup(row_width=3)
day_keyboard.add(*day_buttons)

# Hour keyboard
ampm_buttons = [InlineKeyboardButton("AM", callback_data="set_ampm|AM"),
                InlineKeyboardButton("PM", callback_data="set_ampm|PM"), ]
hour_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_hour|{i}") for i in range(1, 13)]
hour_keyboard = InlineKeyboardMarkup(row_width=3)
hour_keyboard.row(*ampm_buttons)
hour_keyboard.add(*hour_buttons)

# Minute keyboard
minute_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_minute|{i}") for i in range(0, 60, 5)]
minute_keyboard = InlineKeyboardMarkup(row_width=3)
minute_keyboard.add(*minute_buttons)

# Back, Cancel, and Next buttons with their proxies
back_button = InlineKeyboardButton("<< Back", callback_data="back")
cancel_button = InlineKeyboardButton("Cancel", callback_data="cancel")
next_button = InlineKeyboardButton("Next >>", callback_data="next")

year_keyboard.row(back_button, cancel_button, next_button)
month_keyboard.row(back_button, cancel_button, next_button)
day_keyboard.row(back_button, cancel_button, next_button)
hour_keyboard.row(back_button, cancel_button, next_button)
minute_keyboard.row(back_button, cancel_button, next_button)
