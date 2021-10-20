from aiogram import Dispatcher, filters
from aiogram import types as t
from aiogram.dispatcher.filters import Text, state
from aiogram.types import ContentTypes as Ct
from utils import dialog_cal_callback

# from . import log
from . import afisha
from . import afisha as af
from . import help
from . import registration as re
from . import start

# from aiogram.utils.callback_data import CallbackData
# from .afisha import cb_af, inline_timepicker
from .registration import User as U
from .registration import cancel_handler as cancel
from .registration import cb_us, exec_cb
from .registration import settings as reg

# from . import echo


def setup(dp: Dispatcher):

    dp.register_callback_query_handler(af.send_loc, af.locat.filter())
    
    dp.register_callback_query_handler(af.btm,af.bac.filter())
    dp.register_message_handler(
        cancel, filters.Text(equals="cancel", ignore_case=True), state="*"
    )
    dp.register_message_handler(cancel, state="*", commands="cancel")
    dp.register_message_handler(start.bot_start, filters.CommandStart(), state="*")
    # dp.register_message_handler(re.change_state, content_types=Ct.TEXT,state='*')
    dp.register_message_handler(help.bot_help, filters.CommandHelp())
    # dp.register_message_handler(afisha.inline,filters.Regexp("Афиша"))
    dp.register_message_handler(reg, filters.CommandSettings(), state="*")
    dp.register_message_handler(reg, filters.Text(equals="Настройки", ignore_case=True))
    dp.register_message_handler(re.fio, state=U.fio, content_types=Ct.TEXT)
    dp.register_message_handler(re.city, state=U.city, content_types=Ct.TEXT)
    dp.register_message_handler(re.age, state=U.age, content_types=Ct.TEXT)
    dp.register_message_handler(re.nick, state=U.mf_nn, content_types=Ct.TEXT)
    dp.register_message_handler(re.prof, state=U.proof, content_types=Ct.TEXT)
    dp.register_message_handler(re.dohod, state=U.dohod, content_types=Ct.TEXT)
    dp.register_message_handler(re.ph_num, state=U.ph_num, content_types=Ct.CONTACT)
    dp.register_message_handler(re.ph_num_wrong, state=U.ph_num, content_types=Ct.TEXT)
    # dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
    # dp.register_message_handler(log.bot_echo,content_types=Ct.TEXT,state='*', run_task=True)
    dp.register_message_handler(afisha.mp, filters.Text(equals="Афиша"))
    dp.register_callback_query_handler(
        exec_cb, cb_us.filter(action=["ok", "edit", "cancel"]), state=U.allright
    )
    dp.register_message_handler(
        af.cb_bt, filters.Text(equals="Создать"), state=af.main_men.main
    )

    dp.register_message_handler(
        af.afisha_view, filters.Text(equals="Посмотреть"), state=af.main_men.main
    )
    dp.register_message_handler(af.name, state=af.Afs.new)
    dp.register_message_handler(af.decr, state=af.Afs.name)

    dp.register_message_handler(af.loc, state=af.Afs.decr, content_types=Ct.VENUE)
    dp.register_callback_query_handler(
        af.process_dialog_calendar, dialog_cal_callback.filter(), state=af.Afs.location
    )
    dp.register_message_handler(af.mx_user, state=af.Afs.date)
    dp.register_message_handler(
        af.pick_photo, state=af.Afs.users, content_types=Ct.PHOTO
    )
    dp.register_message_handler(
        af.info_photo, content_types=Ct.PHOTO
    )
    dp.callback_query_handler(af.process_dialog_calendar, dialog_cal_callback.filter())
    dp.register_callback_query_handler(
        af.cb_handler, af.inline_timepicker.filter(), state=af.Afs.pick_cal
    )

    # dp.register_callback_query_handler(af.afisha_view, af.applications_cb.filter())
    dp.register_callback_query_handler(af.pages, af.applications_cb.filter())
    dp.register_callback_query_handler(af.zapis_cb, af.zapis.filter())
    dp.register_callback_query_handler(af.coun,af.cou.filter())
        # dp.register_message_handler(af.date, state=af.Afs.users)
