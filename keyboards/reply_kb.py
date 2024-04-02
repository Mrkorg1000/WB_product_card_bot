from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




def get_menu_kb():
    menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/start"),
                KeyboardButton(text="Информация о боте"),
            ],
            [
                KeyboardButton(text="Получить информацию из БД"), 
            ]
        ], resize_keyboard=True,
    )
    return menu_kb