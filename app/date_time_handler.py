from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from .keyboards import year_keyboard, minute_keyboard, hour_keyboard, day_keyboard, month_keyboard
from .main import dp


@dp.callback_query_handler(lambda query: query.data.startswith("set_year|"))
async def set_year(call: CallbackQuery, state: FSMContext):
    year = call.data.split("|")[1]
    await state.update_data(year=year)
    await call.message.edit_reply_markup(year_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith("set_month"))
async def set_month(call: CallbackQuery, state: FSMContext):
    # Extract selected month from callback data
    selected_month = int(call.data.split("|")[1])

    # Update user's state with selected month
    async with state.proxy() as data:
        data['selected_month'] = selected_month

    # Edit message to add a tick emoji near selected month
    selected_month_button = next(filter(lambda b: b.callback_data == call.data, month_keyboard.inline_keyboard[0]))
    selected_month_button.text += " ✅"

    # Answer callback query and edit message with updated keyboard
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=month_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('set_hour|'))
async def process_set_hour(call: CallbackQuery):
    # Get the selected hour from the callback data
    hour = call.data.split('|')[-1]

    # Update the text of the selected hour button to show a tick emoji
    for row in call.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == call.data:
                button.text = f"✅ {hour}"
            else:
                button.text = button.callback_data.split('|')[-1]

    # Answer the callback query and update the inline keyboard message
    await call.answer(call.id)
    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)


@dp.callback_query_handler()
async def next_handler(call: CallbackQuery, state: FSMContext):
    # Get the current keyboard state from the user's State object
    data = await state.get_data()
    current_keyboard = data.get("current_keyboard")

    # Check which keyboard is currently being displayed
    if current_keyboard == "year":
        # If the current keyboard is the year keyboard, switch to the month keyboard
        next_keyboard = "month"
        next_keyboard_markup = month_keyboard
    elif current_keyboard == "month":
        # If the current keyboard is the month keyboard, switch to the day keyboard
        next_keyboard = "day"
        next_keyboard_markup = day_keyboard
    elif current_keyboard == "day":
        # If the current keyboard is the day keyboard, switch to the hour keyboard
        next_keyboard = "hour"
        next_keyboard_markup = hour_keyboard
    elif current_keyboard == "hour":
        # If the current keyboard is the hour keyboard, switch to the minute keyboard
        next_keyboard = "minute"
        next_keyboard_markup = minute_keyboard
    else:
        # If the current keyboard is the minute keyboard, do nothing
        await call.answer("You have already selected the minute!")
        return

    # Update the current keyboard state in the user's State object
    await state.update_data(current_keyboard=next_keyboard)

    # Update the inline keyboard message with the next keyboard markup
    await call.message.edit_reply_markup(reply_markup=next_keyboard_markup)


@dp.callback_query_handler(text="back")
async def back_handler(call: CallbackQuery, state: FSMContext):
    # Get the current keyboard state from the user's State object
    data = await state.get_data()
    current_keyboard = data.get("current_keyboard")

    # Check which keyboard is currently being displayed
    if current_keyboard == "month":
        # If the current keyboard is the month keyboard, switch to the year keyboard
        next_keyboard = "year"
        next_keyboard_markup = year_keyboard
    elif current_keyboard == "day":
        # If the current keyboard is the day keyboard, switch to the month keyboard
        next_keyboard = "month"
        next_keyboard_markup = month_keyboard
    elif current_keyboard == "hour":
        # If the current keyboard is the hour keyboard, switch to the day keyboard
        next_keyboard = "day"
        next_keyboard_markup = day_keyboard
    elif current_keyboard == "minute":
        # If the current keyboard is the minute keyboard, switch to the hour keyboard
        next_keyboard = "hour"
        next_keyboard_markup = hour_keyboard
    else:
        # If the current keyboard is the year keyboard, do nothing
        await call.answer("You can't go back any further!")
        return

    # Update the user's State object with the new keyboard state
    await state.update_data(current_keyboard=next_keyboard)

    # Edit the message with the new keyboard
    await call.message.edit_reply_markup(reply_markup=next_keyboard_markup)

