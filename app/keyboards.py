import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Generate years
current_year = datetime.now().year
years = [str(y) for y in range(current_year, current_year + 5)]
year_buttons = [InlineKeyboardButton(year, callback_data=f"set_year|{year}") for year in years]
year_keyboard = InlineKeyboardMarkup(row_width=3)
year_keyboard.add(*year_buttons)

# Generate months
month_buttons = [InlineKeyboardButton(calendar.month_abbr[i], callback_data=f"set_month|{i}")
                 for i in range(1, 13)
                 ]
month_keyboard = InlineKeyboardMarkup(row_width=3)
month_keyboard.add(*month_buttons)

# Generate days
day_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_day|{i}") for i in range(1, 32)]
day_keyboard = InlineKeyboardMarkup(row_width=7)
day_keyboard.add(*day_buttons)

# Generate hours
hour_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_hour|{i}") for i in range(1, 13)]
hour_keyboard = InlineKeyboardMarkup(row_width=3)
hour_keyboard.add(*hour_buttons)

# Generate AM/PM buttons
ampm_buttons = [InlineKeyboardButton("AM", callback_data="set_ampm|AM"),
                InlineKeyboardButton("PM", callback_data="set_ampm|PM"), ]
ampm_keyboard = InlineKeyboardMarkup(row_width=2)
ampm_keyboard.add(*ampm_buttons)

# Generate minute interval buttons
minute_buttons = [InlineKeyboardButton(str(i), callback_data=f"set_minute|{i}") for i in range(0, 60, 5)]
minute_keyboard = InlineKeyboardMarkup(row_width=12)
minute_keyboard.add(*minute_buttons)
