
from aiogram import Dispatcher, filters,types
from aiogram.dispatcher.filters import Text
from . import help
from . import start
# from . import afisha
# from . import log
from . import registration
from .registration import User
# from aiogram.utils.callback_data import CallbackData

# from . import echo
def setup(dp:Dispatcher):
    dp.register_message_handler(registration.cancel_handler, filters.Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(registration.cancel_handler,state='*', commands='cancel')
    dp.register_message_handler(start.bot_start, filters.CommandStart())
    # dp.register_message_handler(registration.change_state, content_types=types.ContentTypes.TEXT,state='*')
    dp.register_message_handler(help.bot_help, filters.CommandHelp())
    # dp.register_message_handler(afisha.inline,filters.Regexp("Афиша"))
    dp.register_message_handler(registration.settings , filters.CommandSettings(),state="*")
    dp.register_message_handler(registration.settings, filters.Text(equals='Настройки',ignore_case=True))
    dp.register_message_handler(
        registration.fio, state=User.fio, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
    registration.city, state=User.city, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.age, state=User.age, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.nick , state=User.mf_nn, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.prof, state=User.proof, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.dohod, state=User.dohod, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(registration.ph_num, state=User.ph_num, content_types=types.ContentTypes.ANY)
    # dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
    # dp.register_message_handler(log.bot_echo,content_types=types.ContentTypes.TEXT,state='*', run_task=True)
