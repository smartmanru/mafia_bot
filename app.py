from aiogram import Dispatcher
from aiogram.utils import executor

import filters
import handlers
import middlewares
import utils
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher: Dispatcher):
    # Устанавливаем дефолтные команды
    middlewares.setup(dispatcher)
    filters.setup(dispatcher)
    handlers.users.setup(dispatcher)
    await set_default_commands(dispatcher)
    # await utils.start()

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
