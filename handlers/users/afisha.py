import datetime
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.utils.callback_data import CallbackData
from loguru import logger

from data.config import ADMINS as ad
from keyboards.default.main_keyboard import keyboard
from loader import bot
from utils import DialogCalendar
from utils.db_api.psql import afisha_new, get_afisha, get_count, insert_id, checkid
from utils.inline_timepick import InlineTimepicker

inline_timepicker = InlineTimepicker()


def get_afish():
    k = get_afisha()

    afish = []
    for d in range(len(k)):
        j = {}

        # for i in k[d]:
        j["id_af"] = k[d][0]
        j["name"] = k[d][1]
        j["decr"] = k[d][2]
        j["max"] = k[d][3]
        j["loc"] = k[d][4]
        j["date"] = k[d][5]
        j["photo"] = k[d][6]
        j['idushie']=get_count(k[d][0])
        afish.append(j)
    pages_number = len(k)
    return afish


class main_men(StatesGroup):
    main = State()


class Afs(StatesGroup):
    new = State()
    name = State()
    decr = State()
    location = State()
    pick_cal = State()
    date = State()
    users = State()
    pick_photo = State()


applications_cb = CallbackData("applications_list", "page")
applications_manager_page_navigation_cb = CallbackData(
    "application_page_nav", "pages_number"
)

zapis = CallbackData("id", "action")
# class afisha()

cb_af = CallbackData("data", "action")
bac=CallbackData("data","action")
locat = CallbackData("data","lat")

async def mp(message: types.Message):
    keys = []
    if str(message.from_user.id) in ad:
        keys = [["Создать"]]
    keys.append(["Посмотреть"])
    key = await keyboard(keys)
    await message.answer(
        "Выберите действие",
        parse_mode="Markdown",
        reply_markup=key,
        disable_web_page_preview=True,
    )
    await main_men.main.set()


async def pages(query: types.CallbackQuery, callback_data: typing.Dict[any, any]):
    logger.info(query.data)
    plagination_keyboard_list = []
    keyboard_markup = types.InlineKeyboardMarkup()
    afish = get_afish()
    page = int(callback_data["page"])
    pages_number = len(afish)
    index_page = page + 1

    if page > 0:
        previous_page_btn = types.InlineKeyboardButton(
            "⬅️", callback_data=applications_cb.new(page - 1)
        )
        plagination_keyboard_list.append(previous_page_btn)
    a=afish[page]['id_af']
    pages_number_btn = types.InlineKeyboardButton(
        "Записаться",
        callback_data=zapis.new(a),
    )
    plagination_keyboard_list.append(pages_number_btn)

    if index_page < pages_number:
        next_page_btn = types.InlineKeyboardButton(
            "➡️", callback_data=applications_cb.new(page + 1)
        )
        plagination_keyboard_list.append(next_page_btn)
    b=afish[page]['loc']
    logger.info(type(b))
    location_key=types.InlineKeyboardButton("Локация",callback_data=locat.new(b))
    cancel_key=types.InlineKeyboardButton("Назад",callback_data=bac.new("back"))
    

    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(location_key,cancel_key)
    text = afish[page]["name"] + "\n" + afish[page]["decr"]+"\n"+str(afish[page]["idushie"][0][0])+"/"+str(afish[page]["max"])
    ph = types.InputMediaPhoto(media=afish[page]["photo"])
    await query.message.edit_media(ph)
    await query.message.edit_caption(caption=text, reply_markup=keyboard_markup)

async def send_loc(
    query: CallbackQuery, state: FSMContext 
):
    b=query.data.split(":")
    l=b[1].split() 
    long=l[1]
    lat=l[0]
    await query.message.answer_location(longitude=long,latitude=lat)
    
async def btm(
    query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):
    key = await keyboard([["Правила"], ["Афиша", "Рейтинг"], ["Настройки"]])
    await query.message.answer(
    "Добро пожаловать в Бота Maffia by [@Zelova](https://t.me/MafiaZelova)", parse_mode="Markdown",
    reply_markup=key, disable_web_page_preview=True)
    
async def afisha_view(msg: Message, state: FSMContext):
    await state.finish()
    plagination_keyboard_list = []
    afish = get_afish()
    # logger.info(callback_data)
    # logger.info(state)
    # logger.info(query)
    keyboard_markup = types.InlineKeyboardMarkup()
    # logger.info(k)

    # logger.info(afish)

    # await bot.send_message(chat_id=query.from_user.id, text=str(afish))
    page = 0
    allaf = len(afish)

    # keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    # # for page in range(1, pages_number + 1):
    # page_btn = types.InlineKeyboardButton(
    #     page, callback_data=applications_cb.new(page))
    # keyboard_markup.insert(page_btn)

    # back_btn = types.InlineKeyboardButton(
    #     "Назад", callback_data=applications_cb.new(1))
    # keyboard_markup.add(back_btn)

    # # await query.message.edit_text("📖 Пожалуйста, выберите страницу", reply_markup=keyboard_markup)
    # await query.answer()
    pages_number = len(afish)

    if page > 0:
        previous_page_btn = types.InlineKeyboardButton(
            "⬅️", callback_data=applications_cb.new(page - 1)
        )
        plagination_keyboard_list.append(previous_page_btn)

    a=afish[page]['id_af']
    pages_number_btn = types.InlineKeyboardButton(
        "Записаться",
        callback_data=zapis.new(a),
    )
    plagination_keyboard_list.append(pages_number_btn)

    if page < pages_number:
        next_page_btn = types.InlineKeyboardButton(
            "➡️", callback_data=applications_cb.new(page + 1)
        )
        plagination_keyboard_list.append(next_page_btn)

    location_key=types.InlineKeyboardButton("Локация",callback_data=locat.new("loc"))
    cancel_key=types.InlineKeyboardButton("Назад",callback_data=locat.new("back"))

    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(location_key,cancel_key)
    text = afish[page]["name"] + "\n" + afish[page]["decr"]+"\n"+str(afish[page]["idushie"][0][0])+"/"+str(afish[page]["max"])
    # for t in afish:
    await msg.answer_photo(
        photo=afish[page]["photo"],
        caption=text,
        reply_markup=keyboard_markup,
    )

    """

Регистрация        

        """


async def zapis_cb(
    query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):

    logger.info(query)
    l=query.data.split(":")
    k=l[1]
    m=checkid(query.from_user.id,int(k))
    # await query.message.answer(text=m)
    insert_id(query.from_user.id,int(k))
    await query.message.answer(text="Вы записаны на мероприятие. Для оплаты перейдите по ссылке - ссылка")


async def cb_bt(message: Message, state: FSMContext):

    if not str(message.from_user.id) in ad:
        await message.answer("Вы не Админ")
    else:
        await state.finish()
        await Afs.new.set()
        await message.answer(text="Для отмены операции в любой момент наберите /cancel")
        await message.answer(text="Введите название мероприятия")
        async with state.proxy() as data:
            data["id"] = message.chat.id
            data["msg_id"] = message.message_id


async def name(msg: Message, state: FSMContext):
    # markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    # KeyboardButton('Отправить локацию проведения мп', request_location=True))
    async with state.proxy() as data:
        data["mp_name"] = msg.text
    await msg.answer(text="Отправьте описание")
    await Afs.next()


async def decr(msg: Message, state: FSMContext):
    # markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    # KeyboardButton('Отправить локацию проведения мп', request_location=True))
    async with state.proxy() as data:
        data["decr"] = msg.text
    await msg.answer(text="Отправьте геолокацию")
    await Afs.next()


async def loc(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["location"] = [msg.location.latitude, msg.location.longitude]
    await msg.answer(
        "Выберите дату: ", reply_markup=await DialogCalendar().start_calendar()
    )

    await Afs.next()


async def process_dialog_calendar(
    callback_query: CallbackQuery, state: FSMContext, callback_data: dict
):
    selected, date = await DialogCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await callback_query.message.answer(f'Выбрана дата {date.strftime("%d/%m/%Y")}')
        async with state.proxy() as data:
            data["date"] = date.strftime("%d-%m-%Y")
            logger.info(data["date"])
            inline_timepicker.init(
                datetime.time(19),
                datetime.time(1),
                datetime.time(23),
            )
            await bot.send_message(
                callback_query._values["from"].id,
                text="Выбери время",
                reply_markup=inline_timepicker.get_keyboard(),
            )

            await Afs.next()


async def cb_handler(
    query: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext
):
    await query.answer()
    handle_result = inline_timepicker.handle(query.from_user.id, callback_data)

    if handle_result is not None:
        await bot.edit_message_text(
            "Выбрано время "
            + f"{handle_result.hour:02}"
            + ":"
            + f"{handle_result.minute:02}",
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
        )
        await bot.send_message(
            query._values["from"].id, text="Введите макс кол-во юзеров:"
        )
        logger.info(await state.get_state())
        async with state.proxy() as data:
            data["time"] = str(handle_result.hour) + ":" + f"{handle_result.minute:02}"
            await Afs.next()
            logger.info(await state.get_state())

    else:
        await bot.edit_message_reply_markup(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=inline_timepicker.get_keyboard(),
        )


async def mx_user(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["mx_user"] = msg.text
        logger.info(await state.get_state())

        # print(datetime.now())
        # time.mktime(timetuple())
        # times = datetime.time.strptime((data['time']), "H:%M")
        await msg.answer(text="Отправьте фото афиши")
    await Afs.next()
    logger.info(await state.get_state())


async def pick_photo(msg: Message, state: FSMContext):

    async with state.proxy() as data:
        data["photo_id"] = msg.photo[3].file_id
        dt = datetime.datetime.strptime(
            (data["date"]) + " " + data["time"], "%d-%m-%Y %H:%M"
        )
        # dates = datetime.datetime.strptime((data['date']), "%d-%m-%Y%")
        txt = (
            "Мероприятие: "
            + data["mp_name"]
            + "\n"
            + "Расположенной на карте "
            + "\n"
            + "\nМакс игроков:"
            + data["mx_user"]
            + "\nCоздано"
        )
        await msg.answer_location(data["location"][0], data["location"][1])
        await msg.answer(text=txt)
        sql = (
            dt,
            str(data["location"][0]) + " " + str(data["location"][1]),
            data["decr"],
            str(data["mx_user"]),
            data["mp_name"],
            data["photo_id"],
        )
        logger.info(sql)
        # try:
        afisha_new(
            dt,
            str(data["location"][0]) + " " + str(data["location"][1]),
            data["decr"],
            str(data["mx_user"]),
            data["mp_name"],
            data["photo_id"],
        )
        # except:
    #     print(sql)
    # try:
    #     afisha_new(sql)
    # except:
    #     print("переменная не сработала")
    await state.finish()

    # time=datetime.time.strptime(data['date']+data['time'],"%d-%m-%Y%H:%M")

