from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp


async def mp(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))
