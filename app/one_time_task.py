from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from .keyboards import create_year_keyboard, create_keyboard_according_date_type, \
    create_one_time_task_create_task_parameters
from .logger import cc_logger
from .miscellaneous import get_task_text, OneTimeTask, time_parser, prioritized_deletion_of_date
from .task_scheduler import notify_about_task_start


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


def tick_date_type_button(date_date: dict, keyboard: InlineKeyboardMarkup):
    for raw in keyboard.inline_keyboard:
        for button in raw:
            if button.callback_data.startswith('set'):
                button_data = button.callback_data.split('|')

                if button_data[1] == date_date.get(button_data[0].split('_')[1]):
                    button.text += '\u2705'
                    break

            else:
                break


async def add_one_time_task(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    one_time_task_data = data.get('one_time_task')
    if one_time_task_data is None:
        one_time_task_data = dict()
        data['one_time_task'] = one_time_task_data
    await call.message.edit_text("<b>Please enter a name for your task:</b>" + get_task_text(one_time_task_data))

    await state.set_state(OneTimeTask.SETTING_A_NAME)

    await state.update_data(data)


async def edit_task_name(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text("<b>Please send edited name for your task:</b>")

    await state.set_state(OneTimeTask.SETTING_A_NAME)

    await state.update_data(data)


async def enter_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data['one_time_task']['name'] = msg.text

    text = "Choose on of the following options to apply\n" + get_task_text(data["one_time_task"])
    await msg.answer(
        text,
        reply_markup=create_one_time_task_create_task_parameters())

    await state.finish()
    await state.update_data(data)


async def set_date(call: CallbackQuery, state: FSMContext):
    if call.data == 'set_start_date':
        await state.set_state(OneTimeTask.SETTING_A_START_DATE)
    elif call.data == 'set_due_date':
        await state.set_state(OneTimeTask.SETTING_A_DUE_DATE)

    data = await state.get_data()
    one_time_task_data = data.get('one_time_task')

    date_data = await one_time_task_date_state_getter(state, one_time_task_data)

    text = "Let's first select a year!"

    keyboard = create_year_keyboard()
    data['current_keyboard'] = 'year'
    await state.update_data(data)
    tick_date_type_button(date_data, keyboard)

    await call.message.edit_text(text + '\n' + '<code>' + time_parser(date_data) + '</code>', reply_markup=keyboard)


async def base_one_time_task_date_handler(call: CallbackQuery, state: FSMContext):
    """

    :param call:
    :param state:
    :return:
    """

    date_type_prefixed = call.data.split('|')[0]
    data = await state.get_data()
    date_type = date_type_prefixed.split('_')[1]

    one_time_task_data = data['one_time_task']
    date_data = await one_time_task_date_state_getter(state, one_time_task_data)

    new_date_type_keyboard = create_keyboard_according_date_type(date_type, date_data)

    new_date_type_value = call.data.split('|')[1]
    current_date_type_value = date_data.get(date_type)

    if new_date_type_value != current_date_type_value:
        date_data[date_type] = new_date_type_value

    elif new_date_type_value == current_date_type_value:
        date_data[date_type] = None
        prioritized_deletion_of_date(date_data)

    tick_date_type_button(date_data, new_date_type_keyboard)

    if date_type == 'ampm':
        date_type = 'hour'
    data['current_keyboard'] = date_type

    await state.update_data(data)

    return new_date_type_keyboard, date_data


async def date_type_handler(call: CallbackQuery, state: FSMContext):
    keyboard, date_data = await base_one_time_task_date_handler(call, state)

    text_last = call.message.text.find('\n')

    await call.message.edit_text(call.message.text[:text_last] + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                 reply_markup=keyboard)


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
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select a month!' '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'month':

            current_keyboard_value = 'day'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value,
                                                               date_data)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select a day!' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'day':
            current_keyboard_value = 'hour'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select an hour!' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'hour':
            current_keyboard_value = 'minute'
            if date_data.get('ampm') is None:
                await call.answer('Please select a date format')
                return
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select a minute!' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'minute':
            current_keyboard_value = 'task_parameters'
            text = "Choose on of the following options to apply\n" + get_task_text(data["one_time_task"])
            await call.message.edit_text(text, reply_markup=create_one_time_task_create_task_parameters())
            await state.finish()

    data['current_keyboard'] = current_keyboard_value
    await state.update_data(data)


async def back_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_data = await one_time_task_date_state_getter(state, data.get('one_time_task'))
    current_keyboard_value = data.get("current_keyboard")

    # if await check_if_previous(call, date_data, current_keyboard_value) is False:
    #     return

    match current_keyboard_value:
        case 'year':

            current_keyboard_value = 'task_parameters'
            text = "Choose on of the following options to apply\n" + get_task_text(data["one_time_task"])
            await call.message.edit_text(text, reply_markup=create_one_time_task_create_task_parameters())
            await state.finish()

        case 'month':

            current_keyboard_value = 'year'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value,
                                                               date_data)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select a year!' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'day':
            current_keyboard_value = 'month'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select a month!' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'hour':
            current_keyboard_value = 'day'
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value, date_data)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select a day!' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

        case 'minute':
            current_keyboard_value = 'hour'
            if date_data.get('ampm') is None:
                await call.answer('Please select a date format')
                return
            new_keyboard = create_keyboard_according_date_type(current_keyboard_value)
            tick_date_type_button(date_data, new_keyboard)

            await call.message.edit_text('Select an hour' + '\n' + '<code>' + time_parser(date_data) + '</code>',
                                         reply_markup=new_keyboard)

    data['current_keyboard'] = current_keyboard_value
    await state.update_data(data)


async def cancel_date_setting(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_keyboard_value = 'task_parameters'
    text = "Choose on of the following options to apply\n" + get_task_text(data["one_time_task"])
    await call.message.edit_text(text, reply_markup=create_one_time_task_create_task_parameters())
    await state.finish()
    data['current_keyboard'] = current_keyboard_value
    await state.update_data(data)


async def set_description(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    one_time_task_data = data.get('one_time_task')

    await call.message.edit_text("<b>Please enter a description for your task:</b>" + get_task_text(one_time_task_data))

    await state.set_state(OneTimeTask.SETTING_A_DESCRIPTION)
    await state.update_data(data)


async def task_complete(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text('You have completed setting a task, I will tell when to start it')

    data['chat_id'] = call.message.chat.id

    await state.finish()
    await notify_about_task_start(data)



def register_one_time_task_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(add_one_time_task, lambda call: call.data == 'add_one_time_task')

    dp.register_callback_query_handler(edit_task_name, lambda call: call.data == call.data == 'set_name')

    dp.register_message_handler(enter_name, state=OneTimeTask.SETTING_A_NAME)

    dp.register_callback_query_handler(set_date, lambda call: call.data in ['set_start_date', 'set_due_date'])

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

    dp.register_callback_query_handler(cancel_date_setting, lambda call: call.data == 'date_cancel',
                                       state=[OneTimeTask.SETTING_A_START_DATE, OneTimeTask.SETTING_A_DUE_DATE])

    dp.register_callback_query_handler(set_description, lambda call: call.data == 'set_description')

    dp.register_callback_query_handler(set_description, lambda call: call.data == 'set_description',
                                       state=[OneTimeTask.SETTING_A_DESCRIPTION])

    dp.register_callback_query_handler(task_complete, lambda call: call.data == 'complete_task_setting')
