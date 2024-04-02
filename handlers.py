import os
from aiogram import types, F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from keyboards.inline_kb import get_sub_callback_button
from keyboards.reply_kb import get_menu_kb
from pg_db.crud import add_request_to_db, get_5_latest_requests
from pg_db.database import SessionClass
from redis_cl import redis_client
from product_data import *
from dotenv import load_dotenv


db = SessionClass()


load_dotenv()
token = os.getenv("TOKEN")
bot = Bot(token=token)
user_router = Router()


@user_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f'Привет! <b>{message.from_user.first_name}</b>!\n Я могу предоставить тебе информацию\n по продукту с сайта Wildberries \n Введите артикул товара', parse_mode=ParseMode.HTML, reply_markup=get_menu_kb())
    

@user_router.message(F.text == 'Получить информацию из БД')
async def get_db_info(message: types.Message):
    user_id = message.chat.id
    request_list = await get_5_latest_requests(db, user_id)
    text = ''
    for request in request_list:
        string = f'Пользователь: {request.user_id}; время запроса: {request.request_time}; артикул: {request.product_id}\n'
        text += string
    if text == '':
        await message.answer('У Вас нет истории запросов')
    await message.answer(text) 


@user_router.message(F.text == 'Информация о боте')
async def get_db_info(message: types.Message): 
    text = 'Бот принимает на вход артикул товара\n \
            с сайта wildberries и выдает информацию\n \
            о товаре по шаблону:\n \
            <b>Артикул</b>\n \
            <b>Название</b>\n \
            <b>Цена</b>\n \
            <b>Рейтинг товара</b>\n \
            <b>Количество товара НА ВСЕХ СКЛАДАХ</b>\n \
            Также можно подписаться на информацию \n \
            об интересующем товаре. Информаия будет приходить\n \
            каждые 5 минут.\n \
            При нажатии на кнопку "Получить информацию из БД"\n \
            вы получаете информацию о ваших\n \
            5 последних запросах.'  
    await message.answer(text, parse_mode=ParseMode.HTML)
    await message.answer('Введите  артикул товара') 


@user_router.message()
async def product_id_check(message: types.Message): 
    
    try:
        product_id = int(message.text) 
        data = await get_product_data(product_id)
        user_id = message.chat.id
    except ValueError:  
        await message.answer('Введите корректный артикул')
    except AttributeError:  
        await message.answer('Введите корректный артикул')

    else:
        await message.answer(
            f'Информация по товару:\n \
            Артикул <b>{data[1]}</b>\n \
            Название <b>{data[0]}</b>\n \
            Цена <b>{data[2]}</b>\n \
            Рейтинг товара <b>{data[3]}</b>\n \
            Количество товара НА ВСЕХ СКЛАДАХ <b>{data[4]}</b>', \
            parse_mode=ParseMode.HTML, reply_markup=get_sub_callback_button()
        ) 
        
        await add_request_to_db(db=db, user_id=user_id, product_id=product_id)
        await message.answer('Введите  артикул товара')


@user_router.callback_query()
async def callback_data(callback: types.CallbackQuery): 
   
    if callback.data == 'sub':
        user_id = callback.message.chat.id
        product_id = get_articul(callback.message.text)
        await redis_client.set_sub(user_id, product_id)

        await callback.message.answer(
            f'Вы подписались на товар\n с артикулом <b>{product_id}</b>',
            parse_mode=ParseMode.HTML
        )
    
    elif callback.data == 'unsub':
        user_id = callback.message.chat.id
        product_id = get_articul(callback.message.text)
        await redis_client.remove_sub_product(user_id, product_id)

        await callback.message.answer(
            f'Вы отписались от товара\n с артикулом <b>{product_id}</b>',
            parse_mode=ParseMode.HTML
        )
    