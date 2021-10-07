import asyncio
from re import M
from typing import Any

from aiogram import Bot, Dispatcher, filters, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.utils import executor
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (Back, Button, Cancel, Group, Next, Row,
                                        Start)
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_forms import fields, forms
from loguru import logger

import utils
from data import config
from keyboards.default.main_keyboard import keyboard
from loader import bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher: Dispatcher):

    DialogRegistry(dispatcher)
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


class MySG(StatesGroup):
    input = State()
    confirm = State()


async def prew_click(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Going on!")


async def next_click(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Running!")


async def main():
    utils.setup_logger("DEBUG", ["sqlalchemy.engine", "aiogram.bot.api"])
    storage = MemoryStorage()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    registry = DialogRegistry(dp)

    registry.register_start_handler(MySG.input)

    await dp.start_polling()

    registry.register(prew_click)
    registry.register(next_click)


async def bot_start(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        logger.info('c каналом все гуд')
        await message.answer(f"Привет, {message.from_user.full_name}!")
        key = await keyboard([["Правила"], ["Афиша", "Рейтинг"]])
        await message.answer(
            "Test",
            reply_markup=key)
    else:
        channel = await bot.get_chat(config.CHANNEL_ID)
        c_t = channel.title
        c_il = channel.invite_link
        await message.answer(f"{message.from_user.full_name}, у тебя нету подписки на канал "+c_t+" Чтобы подписаться перейди по ссылке "+c_il+"\n \nКак подпишешься - жми снова /start")


class MySG(StatesGroup):
    input = State()
    # context=State()


main_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MySG.input,
)
dialog = Dialog(main_window)


class UserForm(forms.Form):
    LANGUAGE_CHOICES = ('English', 'Russian', 'Chinese')
    LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
        KeyboardButton(label) for label in LANGUAGE_CHOICES
    ])

    name = fields.StringField('Name')
    language = fields.ChoicesField(
        'Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD)
    email = fields.EmailField(
        'Email', validation_error_message='Wrong email format!')


async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))

storage = MemoryStorage()


raw = Row(
    Button(Const("⏮"), id='Prev', on_click=prew_click),
    Button(Const("✅"), id='Ok'),
    Button(Const("⏭"), id='Next', on_click=next_click)
)


async def settings(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["name"] = m.text
    await manager.current_context()
    await dialog.next(manager)
name_dialog = Dialog(
    Window(
        raw,
        MessageInput(str(settings)),
        state=MySG.input,
        # getter=MySG.confirm
    )
)
storage = MemoryStorage()
raw = Row(
    Button(Const("⏮"), id='Prev', on_click=prew_click),
    Button(Const("✅"), id='Ok'),
    Button(Const("⏭"), id='Next', on_click=next_click)
)


async def settings(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["name"] = m.text
    await manager.current_context()
    await dialog.next(manager)
name_dialog = Dialog(
    Window(
        raw,
        MessageInput(str(settings)),
        state=MySG.input,
        # getter=MySG.confirm
    )
)

if __name__ == '__main__':

    asyncio.run(main())
