from aiogram import types
# from aiogram.dispatcher.filters.builtin import CommandStart
from loader import bot
from loguru import logger
from data import config
from aiogram.utils import markdown as md
from keyboards.default.main_keyboard import keyboard
from aiogram.dispatcher import FSMContext
# from .registration import User

async def bot_start(m: types.Message, state:FSMContext):
    user_channel_status= await bot.get_chat_member(chat_id=config.CHANNEL_ID,user_id=m.from_user.id)

    # user_channel_status = await  ('-1001288333015', message.from_user.id)
    if user_channel_status["status"] != 'left':
        logger.info('c каналом все гуд')
        await m.answer(f"Привет, {m.from_user.full_name}!")
        key=await keyboard([["Правила"],["Афиша","Рейтинг"],["Настройки"]])
        await m.answer(
        "Добро пожаловать в Бота Maffia by [@Zelova](https://t.me/MafiaZelova)",parse_mode="Markdown",
        reply_markup=key,disable_web_page_preview=True)
    else:
        channel=await bot.get_chat(config.CHANNEL_ID)
        c_t=channel.title
        c_il=channel.invite_link
        # logger.info(channel)
        await m.answer(f"{m.from_user.full_name}, у тебя нету подписки на канал "+c_t+" Чтобы подписаться перейди по ссылке "+c_il+"\n \nКак подпишешься - жми снова /start")
        await state.set_state("not_subs")



