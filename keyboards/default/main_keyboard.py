from aiogram import types

async def keyboard(buttons:list):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    for i in buttons:
        keyboard.add(*i)
    return(keyboard)