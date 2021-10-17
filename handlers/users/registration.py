import logging
import random
import typing
import uuid
from re import M
from utils.db_api.psql import db_reg
from aiogram import types
from aiogram.dispatcher import FSMContext, storage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from loader import bot
from utils.logger import logging as logger, msg_info as dml
from keyboards.default.main_keyboard import keyboard
from utils.utils_kb import create_button as cr_bt, create_keyboard as cr_kb


class User(StatesGroup):
    page = State()
    fio = State()
    city = State()
    age = State()
    mf_nn = State()
    proof = State()
    dohod = State()
    ph_num = State()
    allright = State()


cb_us = CallbackData("data", "action")


async def cancel_handler(msg: Message, state: FSMContext):
    logger.info(await state.get_state())
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info("Cancelling state %r", current_state)
    await state.finish()
    # And remove keyboard (just in case)
    await msg.reply("Отменено", reply_markup=types.ReplyKeyboardRemove())
    rules = cr_bt("Правила")
    afisha = cr_bt("Афиша")
    reit = cr_bt("Рейтинг")
    settings = cr_bt("Настройки")
    key = cr_kb(rules, afisha, reit, settings)
    await msg.answer(
        "Добро пожаловать в Бота Maffia by [@Zelova](https://t.me/MafiaZelova)",
        parse_mode="Markdown",
        reply_markup=key,
        disable_web_page_preview=True,
    )


async def reg_cb(query: types.CallbackQuery, callback: Message, state: FSMContext):
    dml(callback.message)
    logger.info(await state.get_state())
    await bot.send_message(
        query.message.chat.id,
        text="Для отмены операции в любой момент наберите /cancel",
    )

    await bot.send_message(query.message.chat.id, "Введите Фамилию Имя")
    await User.page.set()
    await User.next()


async def settings(msg: Message, state: FSMContext):
    dml(msg)
    await msg.answer(text="Для отмены операции в любой момент наберите /cancel")
    logger.info(await state.get_state())
    await msg.answer("Введите Фамилию Имя")
    await User.page.set()
    await User.next()


async def fio(msg: types.Message, state: FSMContext):
    dml(msg)

    logger.info(await state.get_state())
    async with state.proxy() as data:
        data["fio"] = msg.text
    await msg.answer("Введите Город")

    await User.next()


async def city(msg: types.Message, state: FSMContext):
    dml(msg)
    logger.info(await state.get_state())
    async with state.proxy() as data:
        data["city"] = msg.text
    await msg.answer("Введите ваш возраст")
    await User.next()


async def age(msg: types.Message, state: FSMContext):
    try:
        int(msg.text)
        dml(msg)
        await msg.answer("Введите Ник для мафии")
        await User.next()
        async with state.proxy() as data:
            data["age"] = msg.text
    except ValueError:
        logger.info("Это не число")
        await msg.answer("Введите ваш возраст цифрами")
        dml(msg)
        logger.info(await state.get_state())


async def nick(msg: types.Message, state: FSMContext):
    dml(msg)
    logger.info(await state.get_state())
    async with state.proxy() as data:
        data["mf_nn"] = msg.text
    await msg.answer("Введите Вашу профессию")
    await User.next()


async def prof(msg: Message, state: FSMContext):
    dml(msg)
    logger.info(await state.get_state())
    async with state.proxy() as data:
        data["proof"] = msg.text
    await msg.answer("Ваш ежемесячный доход от ")
    await User.next()


async def dohod(msg: types.Message, state: FSMContext):
    dml(msg)
    logger.info(await state.get_state())
    async with state.proxy() as data:
        data["dohod"] = msg.text
    markup_request = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    ).add(KeyboardButton("Отправить свой контакт ☎️", request_contact=True))
    await msg.answer(
        'Нажми на кнопку "Отправить свой контакт☎️"', reply_markup=markup_request
    )
    await User.next()


async def ph_num_wrong(msg: types.Message, state: FSMContext):
    markup_request = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    ).add(KeyboardButton("Отправить свой контакт ☎️", request_contact=True))
    await msg.answer('Пока не нажмешь-дальше не пойдешь"', reply_markup=markup_request)


async def ph_num(msg: types.Contact, state: FSMContext):
    logger.info(await state.get_state())
    if msg.content_type == "contact":
        ph_num = msg.contact.phone_number
    else:
        ph_num = msg.text
    async with state.proxy() as data:
        data["ph_num"] = ph_num

    inline_btn_1 = InlineKeyboardButton(
        "⬆️Вернутся назад⬆️", callback_data=cb_us.new(action="edit")
    )
    inline_btn_2 = InlineKeyboardButton(
        "🆗Отправить🆗", callback_data=cb_us.new(action="ok")
    )
    # inline_btn_3 = InlineKeyboardButton(

    # "❌Отменить❌", callback_data=cb_us.new(action='cancel')
    # )
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

    await msg.answer(
        "Проверьте ваши данные: \nФИ: "
        + data["fio"]
        + "\nГород: "
        + data["city"]
        + "\nВозраст: "
        + data["age"]
        + "\nНикнейм для мафии: "
        + data["mf_nn"]
        + "\nПрофессия: "
        + data["proof"]
        + "\nДоход От "
        + data["dohod"]
        + "\nНомер телефона: "
        + data["ph_num"]
        + "\n\nВаш профиль телеграмма и ваше фото будет использоваться в списке участников оплатившую данную игру.\n \nВсе верно?",
        reply_markup=inline_kb1,
    )
    await User.next()
    logger.info(await state.get_state())

    b = []
    l = []
    for k in data:
        b.append(k)
        l.append(data[k])
    k = {}
    for q in range(7):
        k[b[q]] = l[q]
    # logger.info(l)
    # logger.info(k)
    # await msg.answer(k, reply_markup=ReplyKeyboardRemove())
    # db_reg(msg.from_user.id, k.get("fio"), k.get("city"), k.get("age"), k.get(
    #     "mf_nn"), k.get("proof"), k.get("dohod"), k.get("ph_num"))


async def exec_cb(
    query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):
    # await query.answer(query)
    logger.info(await state.get_state())

    callback_data_action = callback_data["action"]
    if callback_data_action == "edit":
        logger.info(callback_data_action)
        async with state.proxy() as data:
            data = []
            await User.first()
            # await bot.delete_message(chat_id=query.message.chat.id,
            #  message_id=query.message.message_id)
            await bot.edit_message_text(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                text="Нажмите:\n/settings - для повторной настройки \n/start для выхода на главную",
            )

            # markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            # KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
            # await bot.send_message(chat_id=query.message.chat.id,reply_markup=markup_request)
            return
    elif callback_data_action == "ok":
        b = []
        l = []
        async with state.proxy() as data:
            for k in data:
                b.append(k)
                l.append(data[k])
            logger.info(l)
            k = {}
            for q in range(7):
                k[b[q]] = l[q]
            logger.info(k)
            # await msg.answer(k, reply_markup=ReplyKeyboardRemove())
        db_reg(
            query.from_user.id,
            k.get("fio"),
            k.get("city"),
            k.get("age"),
            k.get("mf_nn"),
            k.get("proof"),
            k.get("dohod"),
            k.get("ph_num"),
        )

    logger.info(await state.get_state())

    await state.finish()
    logger.info(await state.get_state())
