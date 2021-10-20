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
from utils.db_api.psql import afisha_new, get_afisha, get_count, insert_id, checkid, db_check_reg
from utils.inline_timepick import InlineTimepicker
from utils.utils_kb import create_button as cr_bt, create_keyboard as cr_kb,create_inline_callback_button as cr_incb, create_inline_keyboard as cr_in_kb
inline_timepicker = InlineTimepicker()
async def info_photo(msg:Message):
    logger.info(msg.photo[len(msg.photo)-1].file_id)


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
class Vagon(StatesGroup):
    init = State()
    number = State()


applications_cb = CallbackData("applications_list", "page")
applications_manager_page_navigation_cb = CallbackData(
    "application_page_nav", "pages_number"
)
zapis = CallbackData("id", "action")
# class afisha()
cb_af = CallbackData("data", "action")
bac=CallbackData("back","true")
locat = CallbackData("log","lat")
cou=CallbackData("page","count")

#startafisha
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
    # await main_men.main.set()


#навигация по карточкаа
async def pages(query: types.CallbackQuery,state: FSMContext, callback_data: typing.Dict[any, any]):
    await Vagon.new.set()
 
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
    count=0
    vagons_key=types.InlineKeyboardButton("Приду не один",callback_data=cou.new(count))
    location_key=types.InlineKeyboardButton("Локация",callback_data=locat.new(b))
    cancel_key=types.InlineKeyboardButton("Назад",callback_data=bac.new("back"))
    

    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(location_key,vagons_key,cancel_key)
    text = afish[page]["name"] + "\n" + afish[page]["decr"]+"\n"+str(afish[page]["date"])+"\nЗаписано "+str(afish[page]["idushie"][0][0])+" из "+str(afish[page]["max"])
    ph = types.InputMediaPhoto(media=afish[page]["photo"])
    await query.message.edit_media(ph)
    await query.message.edit_caption(caption=text, reply_markup=keyboard_markup)
async def coun(query: types.CallbackQuery,state: FSMContext, callback_data: typing.Dict[any, any]):
    b=0
    async with state.proxy() as data:
        data["count"] =int(callback_data["count"])
        b=data["count"]
    
    if b<5:
        b+=1
        await bot.answer_callback_query(query.id)
        return b
    else:
        b=0
async def afisha_view(msg: Message, state: FSMContext):
    await state.finish()
    plagination_keyboard_list = []
    afish = get_afish()
    keyboard_markup = types.InlineKeyboardMarkup()
    page = 0
    allaf = len(afish)
    pages_number = len(afish)-1
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
    count=1
    vagons_key=types.InlineKeyboardButton("Приду не один",callback_data=cou.new(count))
    location_key=types.InlineKeyboardButton("Локация",callback_data=locat.new("loc"))
    cancel_key=types.InlineKeyboardButton("Назад",callback_data=bac.new("back"))
    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(location_key,vagons_key,cancel_key)
    text = afish[page]["name"] + "\n" + afish[page]["decr"]+"\n"+str(afish[page]["date"])+"\nЗаписано "+str(afish[page]["idushie"][0][0])+" из "+str(afish[page]["max"])
    await msg.answer_photo(
        photo=afish[page]["photo"],
        caption=text,
        reply_markup=keyboard_markup,
    )
 
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
    
    
    
async def coun(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    query.message.answer(text="Введите число гостей, которые будут с вами от 2 до 5, ввод только цифрами")
    
    """

Регистрация        

        """


async def zapis_cb(
    query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):
    logger.info(query)
    u=db_check_reg(query.from_user.id)
    if u[0][0] is  None:
        await query.message.answer("Введите свои данные в настройках /settings")
        await bot.answer_callback_query(query.id)
        return
    else:
        l=query.data.split(":")
        k=l[1]
        m=checkid(query.from_user.id,int(k))
        logger.info(m)
        if  not m ==[]:
            await query.message.answer("Вы уже записаны на данное мероприятие")
        else:
            insert_id(query.from_user.id,int(k))
            a=types.InlineKeyboardButton(text="Оплатить",url='tg://user?id=1616662464')
            b=types.InlineKeyboardMarkup(row_width=1)
            b.add(a)
            await query.message.answer(reply_markup=b, text="Вы записаны на мероприятие. Для оплаты нажмите на кнопку и ")


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
    async with state.proxy() as data:
        data["mp_name"] = msg.text
    await msg.answer(text="Отправьте описание")
    await Afs.next()


async def decr(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["decr"] = msg.text
    await msg.answer(text="Отправьте геолокацию")
    await Afs.next()


async def loc(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["location"] = [msg.location.latitude, msg.location.longitude]
        data["location_address"] = msg.venue.address
        data["location_title"]=msg.venue.title
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
        b=len(msg.photo)-1
        data["photo_id"] = msg.photo[b].file_id
        dt = datetime.datetime.strptime(
            (data["date"]) + " " + data["time"], "%d-%m-%Y %H:%M"
        )
        # dates = datetime.datetime.strptime((data['date']), "%d-%m-%Y%")
        txt = (
            "Мероприятие: "
            + data["mp_name"]
            + "\n"
            + "Расположенной на карте "
            + data["decr"]+"\n"
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

