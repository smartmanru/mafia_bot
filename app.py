from typing import Any

from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram_dialog import  DialogRegistry, Window
import filters
import handlers
import middlewares
import utils
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher:Dispatcher):
    # Устанавливаем дефолтные команды
    middlewares.setup(dispatcher)
    filters.setup(dispatcher)
    handlers.users.setup(dispatcher)
    DialogRegistry(dispatcher)
    await set_default_commands(dispatcher)
    # await utils.start()
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    utils.setup_logger("DEBUG", ["sqlalchemy.engine", "aiogram.bot.api"])

    executor.start_polling(dp, on_startup=on_startup,skip_updates=False)

