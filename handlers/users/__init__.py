from aiogram import Dispatcher, filters
from . import afisha, help, start, wind

def setup(dp: Dispatcher):
    dp.register_message_handler(help.bot_help, filters.CommandHelp())
    dp.register_message_handler(start.bot_start, filters.CommandStart())
    dp.register_message_handler(wind.settings , filters.CommandSettings())
    # dp.register_message_handler("MainSG.main",filters.CommandSettings())  # resets stack and start dialogs on /start command
    # dp.register_message_handler("name_dialog",)
    # dp.register_message_handler("main_menu",)
    # dp.callback_query_handler()
    # dp.register_message_handler(afisha.inline,filters.Regexp("Афиша"))
    # dp.register_message_handler(
    # dp.register_message_handler(Dialog)
    # dp.register_my_chat_member_handler()
    #     registration.fio, state=meinfo.Q1 ,content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(
    # registration.city, state=meinfo.Q2, content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.age, state=meinfo.Q3, content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.nick , state=meinfo.Q4, content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.prof, state=meinfo.Q5, content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.dohod, state=meinfo.Q6, content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.ph_num, state=meinfo.Q7, content_types=types.ContentTypes.ANY)
   
    # vote_cb = CallbackData('vote')  # post:<action>:<amount>

    # @dp.callback_query_handler(callback="btn1")
    # dp.register_message_handler(
    #     registration.fio, state='ФИО', content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(
    # registration.city, state='Город', content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.age, state='возраст', content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.nick , state='nick', content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.prof, state='prof', content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.dohod, state='dohod', content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(registration.ph_num, state='ph_num', content_types=types.ContentTypes.ANY)
   