import logging
import os

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token=os.environ["BOT_TOKEN"], parse_mode=types.ParseMode.HTML)

# Create a Dispatcher instance
dp = Dispatcher(bot)

# Register handlers here

# Start polling updates from Telegram
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
