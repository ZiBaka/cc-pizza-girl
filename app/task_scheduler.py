import asyncio
from datetime import datetime, timedelta

from aiogram import types, Bot
from celery import Celery

from app.miscellaneous import time_parser, get_task_text

# Create a Celery instance
app = Celery('task_scheduler', broker='amqp://guest:guest@localhost//')


def data_to_date_formatter(data: dict) -> datetime:
    stringed_time = time_parser(data)
    return datetime.strptime(stringed_time, "%I:%M %p %d/%m/%Y")


# Define the Celery task
@app.task(bind=True)
async def notify_about_task_start(self, data: dict):
    bot = Bot.get_current()
    date = data_to_date_formatter(data['one_time_task']['start_date'])

    now = datetime.now()

    time_delta = date - now

    await asyncio.sleep(time_delta.seconds)

    await bot.send_message(chat_id=data.get('chat_id'),
                           text='<b>It is time to start new task!</b>' + get_task_text(data['one_time_task']))

