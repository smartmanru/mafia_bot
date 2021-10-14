import datetime
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext, storage
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove,
                           reply_keyboard)
from aiogram.utils.callback_data import CallbackData
from data.config import ADMINS as ad
from handlers import users
from loader import bot, dp
from loguru import logger
from utils import DialogCalendar, dialog_cal_callback
from utils.inline_timepick import InlineTimepicker

inline_timepicker = InlineTimepicker()
class Afs(StatesGroup):
    new = State()
    name = State()
    location = State()
    pick_cal = State()
    date = State()
    users = State()
class View(StatesGroup):
    page=State()
    

# class afisha()

cb_af = CallbackData('data', 'action')

async def mp(message: types.Message):
    if str(message.from_user.id) in ad:
        inlineafad_btn_1 = InlineKeyboardButton(
            "Создать", callback_data=cb_af.new(action='new'))
        inlineafad_btn_2 = InlineKeyboardButton(
            "Посмотреть", callback_data=cb_af.new(action='view'))
        inlineafad = InlineKeyboardMarkup().add(inlineafad_btn_1, inlineafad_btn_2)
        await message.answer("Выберите действие", reply_markup=inlineafad)
    else:
        await message.answer("new")


async def cb_bt(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    await Afs.new.set()
    await bot.send_message(chat_id=query.from_user.id, text="Введите название мероприятия")
    async with state.proxy() as data:
        data['id'] = query.message.chat.id
        data['msg_id'] = query.message.message_id


async def name(msg: Message, state: FSMContext):
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton('Отправить локацию проведения мп', request_location=True))
    async with state.proxy() as data:
        data['mp_name'] = msg.text
    await msg.answer(text="Введите локацию", reply_markup=markup_request)
    await Afs.next()


async def loc(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = msg.text
    await msg.answer("Выберите дату: ", reply_markup=await DialogCalendar().start_calendar())

    await Afs.next()


async def process_dialog_calendar(callback_query: CallbackQuery, state: FSMContext, callback_data: dict):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Выбрана дата {date.strftime("%d/%m/%Y")}'
        )
        async with state.proxy() as data:
            data['date'] = date.strftime("%d-%m-%Y")
            logger.info(data['date'])
            inline_timepicker.init(
                datetime.time(19),
                datetime.time(1),
                datetime.time(23),)
            await bot.send_message(callback_query._values['from'].id,
                                   text='Выбери время',
                                   reply_markup=inline_timepicker.get_keyboard())

            await Afs.next()

async def cb_handler(query: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext):
    await query.answer()
    handle_result = inline_timepicker.handle(query.from_user.id, callback_data)

    if handle_result is not None:
        await bot.edit_message_text("Выбрано время "+f'{handle_result.hour:02}'+":"+f'{handle_result.minute:02}',
                                    chat_id=query.from_user.id,
                                    message_id=query.message.message_id)
        await bot.send_message(query._values['from'].id, text="Введите макс кол-во юзеров:")
    
        async with state.proxy() as data:
            data['time'] = str(handle_result.hour)+':' + \
                f'{handle_result.minute:02}'
            await Afs.next()
    else:
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=inline_timepicker.get_keyboard())

async def mx_user(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['mx_user'] = msg.text
    txt = "Мероприятие: "+data['mp_name']+"\n"+"В локации "+data['location']+"\n" + \
        data['date']+" числа в "+data['time'] + \
        "\nМакс игроков:"+data['mx_user']+"\nCоздано"
    await msg.answer(text=txt)
