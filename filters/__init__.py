# from aiogram import Dispatcher

# from loader import dp
# # from .is_admin import AdminFilter


# if __name__ == "filters":
#     # dp.filters_factory.bind(AdminFilter)
#     pass

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger
from aiogram import Dispatcher


def setup(dp: Dispatcher):
    # dp.middleware.setup(LoggingMiddleware())
    logger.info('Middlewares are successfully configured')

