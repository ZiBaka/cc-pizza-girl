
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


def time_parser(time_info: dict):
    time_info = f'{time_info.get("hour", "xx")}:' \
                f'{time_info.get("minute", "xx")} ' \
                f'{time_info.get("time_format", "xx")} ' \
                f'{time_info.get("day", "xx")}/' \
                f'{time_info.get("month", "xx")}/' \
                f'{time_info.get("year", "xxxx")}'\

    if time_info != '':
        pass
    return time_info


def get_task_text(task_data: dict) -> str:

    name = task_data.get('name', '')
    start_time = task_data.get('start_date', None)
    due_time = task_data.get('due_date', None)
    description = task_data.get('description', None)
    status = task_data.get('status', None)

    parameters = [f"<b>Name:</b> {name}"]
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


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand('start', 'To start the bot!'),
        BotCommand('help', 'To get instructions!'),
        BotCommand('task', 'To manage tasks!'),
        BotCommand('restart', 'If bot not responding!')
    ])