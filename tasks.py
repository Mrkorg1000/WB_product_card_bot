import asyncio
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode
from aiogram import Bot
from keyboards.inline_kb import get_unsub_callback_button
from product_data import *
from redis_cl import redis_client

load_dotenv()

celery_event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

celery = Celery('tasks',
                broker='redis://localhost:6379/0',
        )

celery.conf.broker_connection_retry_on_startup = True

async def send_sign_up_data_1(product_id, chat_id):
    data = await get_product_data(product_id)
    token = os.getenv("TOKEN")
    bot = Bot(token=token)
    text = f'Информация по товару:\n \
            Артикул <b>{data[1]}</b>\n \
            Название <b>{data[0]}</b>\n \
            Цена <b>{data[2]}</b>\n \
            Рейтинг товара <b>{data[3]}</b>\n \
            Количество товара НА ВСЕХ СКЛАДАХ <b>{data[4]}</b>'
    await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, reply_markup=get_unsub_callback_button())
    await bot.session.close()


async def send_info():
    sub_id_list = await redis_client.get_sub_users()

    for sub_id in sub_id_list:
        products_ids = await redis_client.get_sub_products_ids(sub_id)
        for product_id in products_ids:
            try:
                await send_sign_up_data_1(product_id, sub_id)
            except Exception:
                pass


@celery.task
def start_task() -> None:
    celery_event_loop.run_until_complete(send_info())
    

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/2"), start_task.s())

