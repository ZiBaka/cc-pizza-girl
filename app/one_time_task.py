
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from .keyboards import task_parameters_kb, create_year_keyboard, create_month_keyboard, \
    create_keyboard_according_date_type
from .logger import cc_logger
from .miscellaneous import get_task_text, OneTimeTask


async def one_time_task_date_state_getter(state: FSMContext, one_time_task_data: dict) -> dict:
    current_state = await state.get_state()

    if current_state == OneTimeTask.SETTING_A_START_DATE.state:

        if one_time_task_data.get('start_date') is None:
            one_time_task_data['start_date'] = {}
        return one_time_task_data['start_date']
    elif current_state == OneTimeTask.SETTING_A_DUE_DATE.state:
        if one_time_task_data.get('due_date') is None:
            one_time_task_data['due_date'] = {}
        return one_time_task_data['due_date']
    else:
        cc_logger.info("Current function should be used in SETTING_A_START_DATE and SETTING_A_DUE_DATE contexts!")


async def one_time_task_date_state_setter(state: FSMContext, one_time_task_data: dict, date: dict):
    curren_state = await state.get_state()
    if curren_state == OneTimeTask.SETTING_A_START_DATE.state:
        one_time_task_data['start_date'] = date

    elif curren_state == OneTimeTask.SETTING_A_DUE_DATE.state:
        one_time_task_data['due_date'] = date

    else:
        cc_logger.info("Current function should be used in SETTING_A_START_DATE and SETTING_A_DUE_DATE contexts!")

    await state.update_data(one_time_task_data)


async def check_if_previous(call: CallbackQuery, date_data: dict, current_date_type: str):

    if date_data.get(current_date_type) is None:
        await call.answer(f'Please select the {current_date_type}, before proceeding next step')
        return False


def tick_date_button(new_date, keyboard: InlineKeyboardMarkup, date_type):
    for raw in keyboard.inline_keyboard:
        for button in raw:
            if button.callback_data.startswith(date_type):
                if button.callback_data.split('|')[1] == new_date:
                    button.text += '\u2705'
                    break
            else:
                break

    return keyboard
async def add_one_time_task(call: CallbackQuery, state: FSMContext):
    # Ask the user to enter a name
    await call.message.edit_text("<b>Please enter a name for your task:</b>")

    # Set the "add_task" state to "waiting_for_name"
    await state.set_state(OneTimeTask.SETTING_A_NAME)


async def enter_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data["one_time_task"] = dict()
    data["one_time_task"]["name"] = msg.text

    text = "Choose on of the following options to apply\n" + get_task_text(data["one_time_task"])
    await msg.answer(
        text,
        reply_markup=task_parameters_kb)

    await state.finish()
    await state.update_data(data)


async def set_start_date(call: CallbackQuery, state: FSMContext):

    text = "Let's first enter a year!"
    await call.message.edit_text(text, reply_markup=create_year_keyboard())

    await state.set_state(OneTimeTask.SETTING_A_START_DATE)


async def base_one_time_task_date_handler(call: CallbackQuery, state: FSMContext,
                                          year='2023', month='1'):
    """

    :param call:
    :param state:
    :param month: conditional param to determine the number of day in month of the year
    :param year:  conditional param to determine the number of day in month of the year
    :return:
    """

    date_type_prefixed = call.data.split('|')[0]
    data = await state.get_data()
    date_type = date_type_prefixed.split('_')[1]
    data['current_keyboard'] = date_type
    one_time_task_data = data['one_time_task']
    date_data = await one_time_task_date_state_getter(state, one_time_task_data)
    new_date_type_keyboard = create_keyboard_according_date_type(date_type, year, month)

    new_date_type_value = call.data.split('|')[1]
    current_date_type_value = date_data.get(date_type)

    if new_date_type_value != current_date_type_value:
        tick_date_button(new_date_type_value, new_date_type_keyboard, date_type_prefixed)
        date_data[date_type] = new_date_type_value

    elif new_date_type_value == current_date_type_value:
        date_data[date_type] = None

    await state.update_data(data)

    return new_date_type_keyboard


async def date_type_handler(call: CallbackQuery, state: FSMContext):
    keyboard = await base_one_time_task_date_handler(call, state)
    await call.message.edit_reply_markup(keyboard)


async def next_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_data = await one_time_task_date_state_getter(state, data.get('one_time_task'))
    current_keyboard_value = data.get("current_keyboard")

    if await check_if_previous(call, date_data, current_keyboard_value) is False:
        return

    match current_keyboard_value:
        case 'year':

            current_keyboard_value = 'month'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            new_keyboard = tick_date_button(date_data.get(current_keyboard_value), new_keyboard, current_keyboard_value)

            await call.message.edit_text('Select a month!', reply_markup=new_keyboard)

        case 'month':

            current_keyboard_value = 'day'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value,
                                                               date_data['year'], date_data['month'])
            new_keyboard = tick_date_button(date_data.get(current_keyboard_value), new_keyboard, current_keyboard_value)

            await call.message.edit_text('Select a day!', reply_markup=new_keyboard)

        case 'day':
            current_keyboard_value = 'hour'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            new_keyboard = tick_date_button(date_data.get(current_keyboard_value), new_keyboard, current_keyboard_value)

            await call.message.edit_text('Select an hour!', reply_markup=new_keyboard)

        case 'hour':
            current_keyboard_value = 'minute'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            new_keyboard = tick_date_button(date_data.get(current_keyboard_value), new_keyboard, current_keyboard_value)

            await call.message.edit_text('Select a minute!', reply_markup=new_keyboard)

        case 'minute':
            current_keyboard_value = 'task_parameters'
            text = "Choose on of the following options to apply\n" + get_task_text(data["one_time_task"])
    data['current_keyboard'] = current_keyboard_value
    await state.update_data(data)


async def back_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_data = await one_time_task_date_state_getter(state, data['one_time_task'])
    current_keyboard_value = data.get("current_keyboard")

    if current_keyboard == 'month':

        next_keyboard = 'year'
        year_keyboard = create_year_keyboard()
        selected_year = await one_time_task_date_state_getter(state,data['one_time_task'])
        next_keyboard_markup = tick_date_button(selected_year['year'], year_keyboard, 'set_year')

    elif current_keyboard == 'day':
        # If the current keyboard the day keyboard, switch to the month keyboard
        next_keyboard = "month"
        next_keyboard_markup = create_month_keyboard()
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


def register_one_time_task_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(add_one_time_task, lambda call: call.data == 'add_one_time_task'
                                                                       or call.data == 'set_name')

    dp.register_message_handler(enter_name, state=OneTimeTask.SETTING_A_NAME)

    dp.register_callback_query_handler(set_start_date, lambda call: call.data == 'set_start_date')

    dp.register_callback_query_handler(date_type_handler, lambda call: call.data.startswith("set_year|"),
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(date_type_handler, lambda call: call.data.startswith("set_month|"),
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(date_type_handler, lambda call: call.data.startswith("set_day|"),
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(date_type_handler, lambda call: call.data.startswith("set_hour|"),
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(date_type_handler, lambda call: call.data.startswith("set_ampm|"),
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(date_type_handler, lambda call: call.data.startswith("set_minute|"),
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(back_handler, lambda call: call.data == 'date_back',
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(next_handler, lambda call: call.data == 'date_next',
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])