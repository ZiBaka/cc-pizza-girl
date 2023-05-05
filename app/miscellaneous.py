
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand


class TaskType(StatesGroup):
    ONE_TIME = State()  # for one-time tasks
    YEARLY = State()  # for yearly tasks
    MONTHLY = State()  # for monthly tasks
    DAILY = State()  # for daily tasks
    HOURLY = State()  # for hourly tasks


class OneTimeTask(StatesGroup):

    SETTING_A_NAME = State()
    SETTING_A_START_DATE = State()
    SETTING_A_DUE_DATE = State()
    SETTING_A_DESCRIPTION = State()
    SETTING_A_STATUS = State()


def time_parser(input_time_info: dict) -> str:

    for key, value in input_time_info.copy().items():
        if value is None:
            del input_time_info[key]

    time_info = f'{input_time_info.get("hour", "xx")}:' \
                f'{input_time_info.get("minute", "xx")} ' \
                f'{input_time_info.get("ampm", "xx")} ' \
                f'{input_time_info.get("day", "xx")}/' \
                f'{input_time_info.get("month", "xx")}/' \
                f'{input_time_info.get("year", "xxxx")}'\

    if time_info != '':
        pass
    return time_info


def date_is_completed(date_date: dict):

    required_dates = ('year', 'month', 'week', 'day', 'hour', 'ampm', 'minute')
    for i in required_dates:
        if date_date.get(i) is None:
            return False
        else:
            return True


def prioritized_deletion_of_date(date_data):

    required_order = ('year', 'month', 'week', 'day', 'hour', 'minute')

    for i in required_order:

        if date_data.get(i) is None:
            list_of_items_to_eliminate = required_order[required_order.index(i):]
            for x in list_of_items_to_eliminate:
                if x == 'hour':
                    date_data['ampm'] = None
                date_data[x] = None
            break
        else:
            pass


def get_task_text(task_data: dict) -> str:

    name = task_data.get('name', '')
    start_time = task_data.get('start_date', None)
    due_time = task_data.get('due_date', None)
    description = task_data.get('description', None)
    status = task_data.get('status', None)

    parameters = [f"\n\n<b>Name:</b> <i>{name}</i>"]
    if start_time:
        start_time = time_parser(start_time)
        parameters.append(f"<b>Start Date:</b> {start_time}")

    if due_time:
        due_time = time_parser(due_time)
        parameters.append(f"<b>Due Date:</b> {due_time}")

    if description:
        parameters.append(f"<b>Description:</b> {description}")

    if status:
        parameters.append(f"<b>Status:</b> {status}")

    text = "\n".join(parameters)
    return text


def set_default_commands(dp):
    dp.bot.set_my_commands([
        BotCommand('start', 'To start the bot!'),
        BotCommand('help', 'To get instructions!'),
        BotCommand('task', 'To manage tasks!'),
        BotCommand('restart', 'If bot not responding!')
    ])
