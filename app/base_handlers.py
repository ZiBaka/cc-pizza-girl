from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.keyboards import task_inline_keyboard, create_one_time_task_menu_keyboard
from app.miscellaneous import TaskType, get_task_text, OneTimeTask


async def start_handler(msg: types.Message):
    # The greeting message
    greeting = "Welcome to our time management bot! Use /help to see a list of available commands."

    # Send the greeting message
    await msg.answer(greeting)


async def help_handler(message: types.Message):
    help_text = "Here are the available commands:\n\n" \
                "/start - Start the bot\n" \
                "/help - Show help message\n" \
                "/task - Create a new task\n" \
                "/settings - Change bot settings\n"

    await message.answer(help_text)


async def task_handler(message: types.Message):
    # Send inline keyboard
    await message.answer("Please select a task type:", reply_markup=task_inline_keyboard)


async def one_time_task(call: CallbackQuery):
    # Send a message with buttons
    await call.message.edit_text("Choose on of th options.", reply_markup=create_one_time_task_menu_keyboard())


def register_base_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, Command("start"))
    dp.register_message_handler(help_handler, Command("help"))
    dp.register_message_handler(task_handler, Command("task"))
    dp.register_callback_query_handler(one_time_task, lambda call: call.data == 'one_time_task')

