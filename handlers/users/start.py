from aiogram import types
# from aiogram.dispatcher.filters.builtin import CommandStart
from loader import bot
from loguru import logger
from data import config
from keyboards.default.main_keyboard import keyboard


async def bot_start(message: types.Message):
    user_channel_status= await bot.get_chat_member(chat_id=config.CHANNEL_ID,user_id=message.from_user.id)

    # user_channel_status = await  ('-1001288333015', message.from_user.id)
    if user_channel_status["status"] != 'left':
        logger.info('c каналом все гуд')
        await message.answer(f"Привет, {message.from_user.full_name}!")
        key=await keyboard([["Правила"],["Афиша","Рейтинг"]])
        await message.answer(
        "Добро пожаловать в Бота Maffia by @Zelova",
        reply_markup=key)
        
    else:
        channel=await bot.get_chat(config.CHANNEL_ID)
        c_t=channel.title
        c_il=channel.invite_link
        # logger.info(channel)
        await message.answer(f"{message.from_user.full_name}, у тебя нету подписки на канал "+c_t+" Чтобы подписаться перейди по ссылке "+c_il+"\n \nКак подпишешься - жми снова /start")



