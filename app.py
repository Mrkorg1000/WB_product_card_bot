import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from pg_db.database import engine
from handlers import user_router
from dotenv import load_dotenv
from pg_db.models import Base
from tasks import start_task


load_dotenv()
token = os.getenv("TOKEN")
bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(user_router)


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def on_startup(_):
    start_task.delay()


async def main():
    await start_db()
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, on_startup=on_startup)
    

if __name__ == "__main__":

    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Exit")
    