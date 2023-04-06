import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.base_handlers import register_base_handlers
from app.config import bot_token
from app.miscellaneous import set_default_commands
from app.one_time_task import register_one_time_task_handlers

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)

# Create a Dispatcher instance
dp = Dispatcher(bot, storage=MemoryStorage())
# Register handlers here
register_base_handlers(dp=dp)
register_one_time_task_handlers(dp=dp)

# Start polling updates from Telegram
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
