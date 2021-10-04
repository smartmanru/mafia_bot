
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger
from .throttling import ThrottlingMiddleware
from aiogram import Dispatcher
# from loader import dp

def setup(dp: Dispatcher):
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    logger.info('Middlewares are successfully configured')





# if __name__ == "middlewares":
#     dp.middleware.setup(ThrottlingMiddleware())
