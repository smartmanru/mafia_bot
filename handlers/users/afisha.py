import datetime
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.types.reply_keyboard import KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import text
from data.config import ADMINS as ad
from keyboards.default.main_keyboard import keyboard
from loader import bot
from loguru import logger
from utils import DialogCalendar
from utils.db_api.psql import (afisha_new, all_msg, checkid, db_check_reg,
                               get_afisha, get_afisha_id, get_count, insert_id, update_id, del_mp_db)
from utils.inline_timepick import InlineTimepicker
from utils.utils_kb import create_button as cr_bt
from utils.utils_kb import create_inline_callback_button as cr_incb
from utils.utils_kb import create_inline_keyboard as cr_in_kb
from utils.utils_kb import create_keyboard as cr_kb

inline_timepicker = InlineTimepicker()


async def info_photo(msg: Message):
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
        j['idushie'] = get_count(k[d][0])
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
    inot = State()
    number = State()


applications_cb = CallbackData("applications_list", "page", "vagons")
applications_manager_page_navigation_cb = CallbackData(
    "application_page_nav", "pages_number"
)
zapis = CallbackData("id", "action", "vag")
# class afisha()
cb_af = CallbackData("data", "action")
bac = CallbackData("back", "true")
locat = CallbackData("log", "lat")
cou = CallbackData("page", "count")
req_pay = CallbackData("act", "id", "afish")
delcb = CallbackData("del", "id")
# startafisha


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


# навигация по карточкаа
async def pages(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    all_msg(msg=query.message, callback=query, state=state)

    logger.info(query.data)
    plagination_keyboard_list = []
    keyboard_markup = types.InlineKeyboardMarkup()
    afish = get_afish()
    page = int(callback_data["page"])
    vagons = int(callback_data["vagons"])
    vagons_index = vagons+1
    pages_number = len(afish)
    index_page = page + 1

    if page > 0:
        previous_page_btn = types.InlineKeyboardButton(
            "⬅️", callback_data=applications_cb.new(page - 1, vagons)
        )
        plagination_keyboard_list.append(previous_page_btn)
    a = afish[page]['id_af']
    pages_number_btn = types.InlineKeyboardButton(
        "Записаться",
        callback_data=zapis.new(a, vagons),
    )
    plagination_keyboard_list.append(pages_number_btn)

    if index_page < pages_number:
        next_page_btn = types.InlineKeyboardButton(
            "➡️", callback_data=applications_cb.new(page + 1, vagons)
        )
        plagination_keyboard_list.append(next_page_btn)
    b = afish[page]['loc']
    # logger.info(type(b))

    count_keyboard = []
    if 5 > vagons > 0:
        vagons_minus_key = types.InlineKeyboardButton(
            "-1", callback_data=applications_cb.new(page, vagons-1))
        count_keyboard.append(vagons_minus_key)
    if vagons == 0:
        text = "Я не один"
        vagons_plus_key = types.InlineKeyboardButton(
            text, callback_data=applications_cb.new(page, vagons+1))
        count_keyboard.append(vagons_plus_key)
    else:
        if vagons == 5:
            text = "5-максимум"
            vagons_minus_key = types.InlineKeyboardButton(
                "-1", callback_data=applications_cb.new(page, vagons-1))
            count_keyboard.append(vagons_minus_key)
            vagons_count = types.InlineKeyboardButton(
                text, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
        if vagons < 5:
            vagons_count = types.InlineKeyboardButton(
                vagons, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
            vagons_plus_key = types.InlineKeyboardButton(
                "+1", callback_data=applications_cb.new(page, vagons+1))
            count_keyboard.append(vagons_plus_key)

    location_key = types.InlineKeyboardButton(
        "Локация", callback_data=locat.new(b))
    cancel_key = types.InlineKeyboardButton(
        "Назад", callback_data=bac.new("back"))
    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(*count_keyboard)
    keyboard_markup.row(location_key, cancel_key)
    text = afish[page]["name"] + "\n" + afish[page]["decr"]+"\n" + \
        str(afish[page]["date"])+"\nЗаписано "+str(afish[page]
                                                   ["idushie"][0][0])+" из "+str(afish[page]["max"])
    if str(query.message.chat.id) in ad:
        del_key = types.InlineKeyboardButton(
            "Удалить", callback_data=delcb.new(afish[page]["id_af"]))
        keyboard_markup.row(del_key)

    ph = types.InputMediaPhoto(media=afish[page]["photo"])

    await query.message.edit_media(ph)

    await query.message.edit_caption(caption=text, reply_markup=keyboard_markup)


async def del_mp(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    id = callback_data["id"]
    del_mp_db(int(id))
    await query.message(text="Вы удалили событие нажмите /start для продолжение")


async def couni(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    async with state.proxy() as data:
        data["count"] = int(callback_data["count"])
        b = data["count"]

    if b < 5:
        b += 1
        await bot.answer_callback_query(query.id)
        return b
    else:
        b = 0


async def afisha_view(msg: Message, state: FSMContext):
    await state.finish()
    plagination_keyboard_list = []
    afish = get_afish()
    keyboard_markup = types.InlineKeyboardMarkup()
    page = 0
    vagons = 0
    index_page = page + 1
    allaf = len(afish)
    pages_number = len(afish)
    if page > 0:
        previous_page_btn = types.InlineKeyboardButton(
            "⬅️", callback_data=applications_cb.new(page + 1, vagons)
        )
        plagination_keyboard_list.append(previous_page_btn)
    a = afish[page]['id_af']
    pages_number_btn = types.InlineKeyboardButton(
        "Записаться",
        callback_data=zapis.new(a, vagons),
    )
    plagination_keyboard_list.append(pages_number_btn)

    if index_page < pages_number:
        next_page_btn = types.InlineKeyboardButton(
            "➡️", callback_data=applications_cb.new(page + 1, vagons)
        )
        plagination_keyboard_list.append(next_page_btn)
    b = afish[page]['loc']
    # logger.info(type(b))
    count_keyboard = []
    if 5 > vagons > 0:
        vagons_minus_key = types.InlineKeyboardButton(
            "-1", callback_data=applications_cb.new(page, vagons-1))
        count_keyboard.append(vagons_minus_key)
    if vagons == 0:
        text = "Я не один"
        vagons_plus_key = types.InlineKeyboardButton(
            text, callback_data=applications_cb.new(page, vagons+1))
        count_keyboard.append(vagons_plus_key)
    else:
        if vagons == 5:
            text = "5-максимум"
            vagons_minus_key = types.InlineKeyboardButton(
                "-1", callback_data=applications_cb.new(page, vagons-1))
            count_keyboard.append(vagons_minus_key)
            vagons_count = types.InlineKeyboardButton(
                text, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
        if vagons < 5:
            vagons_count = types.InlineKeyboardButton(
                vagons, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
            vagons_plus_key = types.InlineKeyboardButton(
                "+1", callback_data=applications_cb.new(page, vagons+1))
            count_keyboard.append(vagons_plus_key)
    location_key = types.InlineKeyboardButton(
        "Локация", callback_data=locat.new(b))
    cancel_key = types.InlineKeyboardButton(
        "Назад", callback_data=bac.new("back"))
    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(*count_keyboard)
    keyboard_markup.row(location_key, cancel_key)
    text = afish[page]["name"] + "\n" + afish[page]["decr"]+"\n" + \
        str(afish[page]["date"])+"\nЗаписано "+str(afish[page]
                                                   ["idushie"][0][0])+" из "+str(afish[page]["max"])
    await msg.answer_photo(
        photo=afish[page]["photo"],
        caption=text,
        reply_markup=keyboard_markup,
    )


async def send_loc(
    query: CallbackQuery, state: FSMContext
):
    b = query.data.split(":")
    l = b[1].split()
    long = l[1]
    lat = l[0]
    await query.message.answer_location(longitude=long, latitude=lat)


async def btm(
    query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):
    key = await keyboard([["Правила"], ["Афиша", "Рейтинг"], ["Настройки"]])
    await query.message.answer(
        "Добро пожаловать в Бота Mafia by [@Zelova](https://t.me/MafiaZelova)", parse_mode="Markdown",
        reply_markup=key, disable_web_page_preview=True)


async def coun(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    query.message.answer(
        text="Введите число гостей, которые будут с вами от 2 до 5, ввод только цифрами")

    """

Регистрация

        """


async def zapis_cb(
    query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):
    logger.info(query)
    u = db_check_reg(query.from_user.id)
    keyboard_markup = types.InlineKeyboardMarkup()

    if u[0][7] is None:
        await query.message.answer("Введите свои данные в настройках /settings")
        await bot.answer_callback_query(query.id)
        return
    else:
        l = query.data.split(":")
        k = l[1]
        s = l[2]
        m = checkid(query.from_user.id, int(k))
        logger.info(m)
        if not m == []:
            if m[0][5]:
                await query.message.answer("Вы уже записаны на данное мероприятие")
            else:
                await query.message.answer('Вы еще не оплатили это мероприятие')
        else:
            key = []
            insert_id(query.from_user.id, int(k), int(s),)
            a = types.InlineKeyboardButton(
                text="Оплатить", url='tg://user?id=1616662464')
            b = types.InlineKeyboardMarkup(row_width=1)
            id = get_afisha_id(int(k))
            nameMp = id[0][0]
            date = str(id[0][1])
            b.add(a)
            text = "Пользователь @"+u[0][0]+"\n создал заявку на оплату."+nameMp + " на дату "+date+"\n Его данные:\nФИО-"+u[0][1]+"\n"+u[0][2]+"\nВозраст: "+str(
                u[0][3])+"\nПрофессия:"+u[0][4]+"\nДоход от "+u[0][5]+"\nНомер телефона: "+u[0][6]+"\nИгровой ник:"+u[0][7]+"\nОн с собой привел +"+s

            suc = types.InlineKeyboardButton(text="Одобрить", callback_data=req_pay.new(
                query.from_user.id, int(k)))
            # key.append(suc)
            cancel = types.InlineKeyboardButton(
                text='Отменить', callback_data=req_pay.new("gavno", "her"))
            # key.append(cancel)
            keyboard_markup.row(suc)
            await bot.send_message(chat_id=881691, text=text, reply_markup=keyboard_markup)
            await query.message.answer(reply_markup=b, text="Вы записаны на мероприятие. Для оплаты нажмите на кнопку и запросите оплату")


async def confirm(query: types.CallbackQuery, callback_data: typing.Dict[any, any]
                  ):
    l = list(query.data.split(":"))
    k = l[1]
    s = l[2]
    logger.info(k+s)
    update_id(int(k), int(s))
    await bot.send_message(chat_id=k, text="Оплата прошла и подтверждена нажмите /start для продолжения")


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
        data["location_title"] = msg.venue.title
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
            data["time"] = str(handle_result.hour) + ":" + \
                f"{handle_result.minute:02}"
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
        b = len(msg.photo)-1
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
