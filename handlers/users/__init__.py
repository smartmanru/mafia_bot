from loguru import logger
from aiogram import Dispatcher, filters,types
from . import help
from . import start
from . import afisha
from . import registration
from aiogram.utils.callback_data import CallbackData

# from . import echo
def setup(dp: Dispatcher):
    dp.register_message_handler(help.bot_help, filters.CommandHelp())
    dp.register_message_handler(start.bot_start, filters.CommandStart())
    # dp.register_message_handler(afisha.inline,filters.Regexp("Афиша"))
    dp.register_message_handler(registration.settings , filters.CommandSettings())
    dp.register_message_handler(
        registration.fio, state='ФИО', content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
    registration.city, state='Город', content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.age, state='возраст', content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.nick , state='nick', content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.prof, state='prof', content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.dohod, state='dohod', content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.ph_num, state='ph_num', content_types=types.ContentTypes.ANY)
    dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))