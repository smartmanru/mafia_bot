import asyncio
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import executor
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Group, Next, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

import filters
import handlers
import middlewares
import utils
from data import config
from loader import dp

# from utils.notify_admins import on_startup_notify
# from utils.set_bot_commands import set_default_commands
# from handlers.users.wind import prew_click,  next_click, MySG

# async def on_startup(dispatcher:Dispatcher):
    # Устанавливаем дефолтные команды
    # DialogRegistry(dispatcher)
    # await set_default_commands(dispatcher)
    # # await utils.start()
    # await on_startup_notify(dispatcher)
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
    middlewares.setup(dp)
    filters.setup(dp)
    handlers.users.setup(dp)
    registry.register_start_handler(MySG.input)  # resets stack and start dialogs on /start command
    registry.register(prew_click)
    registry.register(next_click)

    await dp.start_polling()

if __name__ == '__main__':

    asyncio.run(main())

#     executor.start_polling(dp, on_startup=on_startup,skip_updates=False)

# bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
