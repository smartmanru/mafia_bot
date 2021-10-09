
import logging
import random
import typing
import uuid
from re import M

from aiogram import types
from aiogram.dispatcher import FSMContext, storage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from loader import bot
from utils.logger import logging as logger


class User(StatesGroup):
    page = State()
    fio = State()
    city = State()
    age = State()
    mf_nn = State()
    proof = State()
    dohod = State()
    ph_num = State()


cb_us = CallbackData('data', 'action')


async def cancel_handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info('Cancelling state %r', current_state)
    await state.finish()
    # And remove keyboard (just in case)
    await msg.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())


async def settings(msg: Message, state: FSMContext):
    await msg.answer('Введите Фамилию Имя')
    await User.page.set()
    await User.next()


async def fio(msg: types.Message, state: FSMContext):
    logger.info(User.page)
    async with state.proxy() as data:
        data['fio'] = msg.text
    await msg.answer('Введите Город')
    await User.next()


async def city(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = msg.text
    await msg.answer('Введите ваш возраст')
    await User.next()


async def age(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = msg.text
    await msg.answer('Введите Ник для мафии')
    await User.next()


async def nick(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mf_nn'] = msg.text
    await msg.answer('Введите Вашу профессию')
    await User.next()


async def prof(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['proof'] = msg.text
    await msg.answer('Ваш ежемесячный доход от ')
    await User.next()


async def dohod(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dohod'] = msg.text
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
    await msg.answer('Ведите ваш номер телефона', reply_markup=markup_request)
    await User.next()


async def ph_num(msg: types.Contact, state: FSMContext):
    if msg.content_type == 'contact':
        ph_num = msg.contact.phone_number
    else:
        ph_num = msg.text
    async with state.proxy() as data:
        data['ph_num'] = ph_num

    inline_btn_1 = InlineKeyboardButton(
        "🖌Изменить🖌", callback_data=cb_us.new(action='edit'))
    inline_btn_2 = InlineKeyboardButton(
        "☑️Все Ок☑️", callback_data=cb_us.new(action='ok'))
    inline_btn_3 = InlineKeyboardButton(
        "❌Отменить❌", callback_data=cb_us.new(action='cancel'))
    inline_kb1 = InlineKeyboardMarkup().add(
        inline_btn_1, inline_btn_2, inline_btn_3)
    await msg.answer("Проверьте ваши данные: \nФИ: "+data['fio']+"\nГород: "+data['city']+"\nВозраст: "+data['age']+"\nНикнейм для мафии: "+data['mf_nn']+"\nПрофессия: "+data['proof']+"\nДоход От "+data['dohod']+"\nНомер телефона: "+data['ph_num']+"\n\nВаш профиль телеграмма и ваше фото будет использоваться в списке участников оплатившую данную игру.\n \nВсе верно?", reply_markup=inline_kb1)
    b = []
    l = []
    for k in data:
        b.append(data)
        l.append(data[k])
    logger.info(b+l)
    u = b+l
    k = str(u)
    await msg.answer(k, reply_markup=ReplyKeyboardRemove)
    await state.finish()


async def exec_cb(query: types.CallbackQuery, callback_data: typing.Dict[any, any]):
    # await query.answer(query)
    callback_data_action = callback_data['action']
    if callback_data_action == "edit":
        logger.info(callback_data_action)
        set.state
