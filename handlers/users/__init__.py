
from aiogram import Dispatcher, filters, types
from aiogram.dispatcher.filters import Text
from . import help
from . import start
from . import afisha
# from . import log
from . import registration
from .registration import User as U, exec_cb, cb_us, settings as reg, cancel_handler as cancel
# from aiogram.utils.callback_data import CallbackData

# from . import echo


def setup(dp: Dispatcher):
    dp.register_message_handler(cancel, filters.Text(
        equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(cancel, state='*', commands='cancel')
    dp.register_message_handler(start.bot_start, filters.CommandStart())
    # dp.register_message_handler(registration.change_state, content_types=types.ContentTypes.TEXT,state='*')
    dp.register_message_handler(help.bot_help, filters.CommandHelp())
    # dp.register_message_handler(afisha.inline,filters.Regexp("Афиша"))
    dp.register_message_handler(reg, filters.CommandSettings(), state="*")
    dp.register_message_handler(reg, filters.Text(
        equals='Настройки', ignore_case=True))
    dp.register_message_handler(
        registration.fio, state=U.fio, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        registration.city, state=U.city, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        registration.age, state=U.age, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        registration.nick, state=U.mf_nn, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        registration.prof, state=U.proof, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        registration.dohod, state=U.dohod, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        registration.ph_num, state=U.ph_num, content_types=types.ContentTypes.ANY)
    # dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
    # dp.register_message_handler(log.bot_echo,content_types=types.ContentTypes.TEXT,state='*', run_task=True)
    dp.register_message_handler(afisha.mp, filters.Text(equals='Афиша'))

    dp.register_callback_query_handler(
        exec_cb, cb_us.filter(action=['ok', 'edit', 'cancel']))
