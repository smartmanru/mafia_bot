import datetime
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.callback_data import CallbackData
from data.config import ADMINS as ad
from keyboards.default.main_keyboard import keyboard
from loader import bot
from loguru import logger
from utils import DialogCalendar
from utils.db_api.psql import (db_af_new, db_log_upd, db_idu_chk_reg, db_reg_sel_all_user,
                               db_af_sel, db_af_sel_id, db_idu_sel_count, db_idu_new_zap, db_idu_upd_pay, db_idu_del)
from utils.inline_timepick import InlineTimepicker
from utils.geocoder import geocoder

inline_timepicker = InlineTimepicker()


async def info_photo(msg: Message):
    logger.info(msg.photo[len(msg.photo) - 1].file_id)


def get_afish():
    k = db_af_sel()

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
        j['idushie'] = db_idu_sel_count(k[d][0])
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
        keys = [["??????????????"]]
    keys.append(["????????????????????"])
    key = await keyboard(keys)
    await message.answer(
        "???????????????? ????????????????",
        parse_mode="Markdown",
        reply_markup=key,
        disable_web_page_preview=True,
    )
    await main_men.main.set()


# ?????????????????? ???? ??????????????????
async def pages(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    db_log_upd(msg=query.message, callback=query, state=state)

    logger.info(query.data)
    plagination_keyboard_list = []
    keyboard_markup = types.InlineKeyboardMarkup()
    afish = get_afish()

    page = int(callback_data["page"])
    vagons = int(callback_data["vagons"])
    pages_number = len(afish)
    index_page = page + 1

    if page > 0:
        previous_page_btn = types.InlineKeyboardButton(
            "??????", callback_data=applications_cb.new(page - 1, vagons)
        )
        plagination_keyboard_list.append(previous_page_btn)
    a = afish[page]['id_af']
    if int(afish[page]["idushie"]) < int(afish[page]["max"]):
        pages_number_btn = types.InlineKeyboardButton(
            "????????????????????",
            callback_data=zapis.new(a, vagons),
        )
        plagination_keyboard_list.append(pages_number_btn)

    if index_page < pages_number:
        next_page_btn = types.InlineKeyboardButton(
            "??????", callback_data=applications_cb.new(page + 1, vagons)
        )
        plagination_keyboard_list.append(next_page_btn)
    b = afish[page]['loc']

    count_keyboard = []
    if 5 > vagons > 0:
        vagons_minus_key = types.InlineKeyboardButton(
            "-1", callback_data=applications_cb.new(page, vagons - 1))
        count_keyboard.append(vagons_minus_key)
    if vagons == 0:
        text = "?? ???? ????????"
        vagons_plus_key = types.InlineKeyboardButton(
            text, callback_data=applications_cb.new(page, vagons + 1))
        count_keyboard.append(vagons_plus_key)
    else:
        if vagons == 5:
            text = "5-????????????????"
            vagons_minus_key = types.InlineKeyboardButton(
                "-1", callback_data=applications_cb.new(page, vagons - 1))
            count_keyboard.append(vagons_minus_key)
            vagons_count = types.InlineKeyboardButton(
                text, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
        if vagons < 5:
            vagons_count = types.InlineKeyboardButton(
                vagons, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
            vagons_plus_key = types.InlineKeyboardButton(
                "+1", callback_data=applications_cb.new(page, vagons + 1))
            count_keyboard.append(vagons_plus_key)

    location_key = types.InlineKeyboardButton(
        "??????????????", callback_data=locat.new(b))
    cancel_key = types.InlineKeyboardButton(
        "??????????", callback_data=bac.new("back"))
    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(*count_keyboard)
    keyboard_markup.row(location_key, cancel_key)
    text = str(afish[page]["id_af"]) + "\n" + afish[page]["name"] + "\n" + afish[page]["decr"] + "\n" + \
           str(afish[page]["date"]) + "\n???????????????? " + str(afish[page]
                                                          ["idushie"]) + " ???? " + str(afish[page]["max"])
    if str(query.message.chat.id) in ad:
        del_key = types.InlineKeyboardButton(
            "??????????????", callback_data=delcb.new(afish[page]["id_af"]))
        keyboard_markup.row(del_key)
    ph = types.InputMediaPhoto(media=afish[page]["photo"])
    await query.message.edit_media(ph)
    await query.message.edit_caption(caption=text, reply_markup=keyboard_markup)


async def del_mp(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    id = callback_data["id"]
    db_idu_del(int(id))
    await query.message(text="???? ?????????????? ?????????????? ?????????????? /start ?????? ??????????????????????")


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
            "??????", callback_data=applications_cb.new(page - 1, vagons)
        )
        plagination_keyboard_list.append(previous_page_btn)
    a = afish[page]['id_af']
    if int(afish[page]["idushie"]) < int(afish[page]["max"]):
        pages_number_btn = types.InlineKeyboardButton(
            "????????????????????",
            callback_data=zapis.new(a, vagons),
        )
        plagination_keyboard_list.append(pages_number_btn)

    if index_page < pages_number:
        next_page_btn = types.InlineKeyboardButton(
            "??????", callback_data=applications_cb.new(page + 1, vagons)
        )
        plagination_keyboard_list.append(next_page_btn)
    b = afish[page]['loc']
    # logger.info(type(b))

    count_keyboard = []
    if 5 > vagons > 0:
        vagons_minus_key = types.InlineKeyboardButton(
            "-1", callback_data=applications_cb.new(page, vagons - 1))
        count_keyboard.append(vagons_minus_key)
    if vagons == 0:
        text = "?? ???? ????????"
        vagons_plus_key = types.InlineKeyboardButton(
            text, callback_data=applications_cb.new(page, vagons + 1))
        count_keyboard.append(vagons_plus_key)
    else:
        if vagons == 5:
            text = "5-????????????????"
            vagons_minus_key = types.InlineKeyboardButton(
                "-1", callback_data=applications_cb.new(page, vagons - 1))
            count_keyboard.append(vagons_minus_key)
            vagons_count = types.InlineKeyboardButton(
                text, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
        if vagons < 5:
            vagons_count = types.InlineKeyboardButton(
                vagons, callback_data=applications_cb.new(page, vagons))
            count_keyboard.append(vagons_count)
            vagons_plus_key = types.InlineKeyboardButton(
                "+1", callback_data=applications_cb.new(page, vagons + 1))
            count_keyboard.append(vagons_plus_key)

    location_key = types.InlineKeyboardButton(
        "??????????????", callback_data=locat.new(b))
    cancel_key = types.InlineKeyboardButton(
        "??????????", callback_data=bac.new("back"))
    keyboard_markup.row(*plagination_keyboard_list)
    keyboard_markup.row(*count_keyboard)
    keyboard_markup.row(location_key, cancel_key)
    text = str(afish[page]["id_af"]) + "\n" + afish[page]["name"] + "\n" + afish[page]["decr"] + "\n" + \
           str(afish[page]["date"]) + "\n???????????????? " + str(afish[page]
                                                          ["idushie"]) + " ???? " + str(afish[page]["max"])
    if str(msg.chat.id) in ad:
        del_key = types.InlineKeyboardButton(
            "??????????????", callback_data=delcb.new(afish[page]["id_af"]))
        keyboard_markup.row(del_key)
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
    key = await keyboard([["??????????????"], ["??????????", "??????????????"], ["??????????????????"]])
    await query.message.answer(
        "?????????? ???????????????????? ?? ???????? Mafia by [@Zelova](https://t.me/MafiaZelova)", parse_mode="Markdown",
        reply_markup=key, disable_web_page_preview=True)


async def coun(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]):
    query.message.answer(
        text="?????????????? ?????????? ????????????, ?????????????? ?????????? ?? ???????? ???? 2 ???? 5, ???????? ???????????? ??????????????")

    """

??????????????????????

        """


async def zapis_cb(
        query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[any, any]
):
    logger.info(query)
    u = db_reg_sel_all_user(query.from_user.id)
    keyboard_markup = types.InlineKeyboardMarkup()

    if u[0][7] is None:
        await query.message.answer("?????????????? ???????? ???????????? ?? ???????????????????? /settings")
        await bot.answer_callback_query(query.id)
        return
    else:
        l = query.data.split(":")
        k = l[1]
        s = l[2]
        m = db_idu_chk_reg(query.from_user.id, int(k))
        logger.info(m)
        if not m == []:
            if m[0][5]:
                await query.message.answer("???? ?????? ???????????????? ???? ???????????? ??????????????????????")
            else:
                await query.message.answer('???? ?????? ???? ???????????????? ?????? ??????????????????????')
        else:
            key = []
            db_idu_new_zap(query.from_user.id, int(k), int(s), )
            a = types.InlineKeyboardButton(
                text="????????????????", url='tg://user?id=1616662464')
            b = types.InlineKeyboardMarkup(row_width=1)
            id = db_af_sel_id(int(k))
            nameMp = id[0][0]
            date = str(id[0][1])
            b.add(a)
            text = "???????????????????????? @" + u[0][
                0] + "\n ???????????? ???????????? ???? ????????????." + nameMp + " ???? ???????? " + date + "\n ?????? ????????????:\n??????-" + u[0][
                       1] + "\n" + u[0][2] + "\n??????????????: " + str(
                u[0][3]) + "\n??????????????????:" + u[0][4] + "\n?????????? ???? " + u[0][5] + "\n?????????? ????????????????: " + u[0][
                       6] + "\n?????????????? ??????:" + u[0][7] + "\n???? ?? ?????????? ???????????? +" + s

            suc = types.InlineKeyboardButton(text="????????????????", callback_data=req_pay.new(
                query.from_user.id, int(k)))
            # key.append(suc)
            cancel = types.InlineKeyboardButton(
                text='????????????????', callback_data=req_pay.new("gavno", "her"))
            # key.append(cancel)
            keyboard_markup.row(suc)
            await bot.send_message(chat_id=881691, text=text, reply_markup=keyboard_markup)
            await query.message.answer(reply_markup=b,
                                       text="???? ???????????????? ???? ??????????????????????. ?????? ???????????? ?????????????? ???? ???????????? ?? ?????????????????? ????????????")


async def confirm(query: types.CallbackQuery, callback_data: typing.Dict[any, any]
                  ):
    l = list(query.data.split(":"))
    k = l[1]
    s = l[2]
    logger.info(k + s)
    db_idu_upd_pay(int(k), int(s))
    await bot.send_message(chat_id=k, text="???????????? ???????????? ?? ???????????????????????? ?????????????? /start ?????? ??????????????????????")


async def cb_bt(message: Message, state: FSMContext):
    if not str(message.from_user.id) in ad:
        await message.answer("???? ???? ??????????")
    else:
        await state.finish()
        await Afs.new.set()
        await message.answer(text="?????? ???????????? ???????????????? ?? ?????????? ???????????? ???????????????? /cancel")
        await message.answer(text="?????????????? ???????????????? ??????????????????????")
        async with state.proxy() as data:
            data["id"] = message.chat.id
            data["msg_id"] = message.message_id


async def name(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["mp_name"] = msg.text
    await msg.answer(text="?????????????????? ????????????????")
    await Afs.next()


async def decr(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["decr"] = msg.text
    await msg.answer(text="?????????????????? ????????????????????")
    await Afs.next()


async def loc(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.content_type == "text":
            a = geocoder(msg.text)

            l = a.split()
            long = l[0]
            lat = l[1]
            data["location"]=[lat,long]
            await msg.answer_location(longitude=long,latitude=lat)

        elif msg.content_type == "venue":
            data["location"] = [msg.location.latitude, msg.location.longitude]
            data["location_address"] = msg.venue.address
            data["location_title"] = msg.venue.title
        elif msg.content_type == "location":
            data["location"]=[msg.location.latitude,msg.location.longitude]
        if data["location"]:
            await msg.answer(
                "???????????????? ????????: ", reply_markup=await DialogCalendar().start_calendar()
            )

            await Afs.next()
        else:msg.answer("???? ???? ?????????? ??????????????")

async def process_dialog_calendar(
        callback_query: CallbackQuery, state: FSMContext, callback_data: dict
):
    selected, date = await DialogCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await callback_query.message.answer(f'?????????????? ???????? {date.strftime("%d/%m/%Y")}')
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
                text="???????????? ??????????",
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
            "?????????????? ?????????? "
            + f"{handle_result.hour:02}"
            + ":"
            + f"{handle_result.minute:02}",
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
        )
        await bot.send_message(
            query._values["from"].id, text="?????????????? ???????? ??????-???? ????????????:"
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
        await msg.answer(text="?????????????????? ???????? ??????????")
    await Afs.next()
    logger.info(await state.get_state())


async def pick_photo(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        b = len(msg.photo) - 1
        data["photo_id"] = msg.photo[b].file_id
        dt = datetime.datetime.strptime(
            (data["date"]) + " " + data["time"], "%d-%m-%Y %H:%M"
        )
        # dates = datetime.datetime.strptime((data['date']), "%d-%m-%Y%")
        txt = (
                "??????????????????????: "
                + data["mp_name"]
                + "\n"
                + "?????????????????????????? ???? ?????????? "
                + data["decr"] + "\n"
                + "\n???????? ??????????????:"
                + data["mx_user"]
                + "\nC????????????"
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
        db_af_new(
            dt,
            str(data["location"][0]) + " " + str(data["location"][1]),
            data["decr"],
            str(data["mx_user"]),
            data["mp_name"],
            data["photo_id"],
        )
        await state.finish()

        # except:
    #     print(sql)
    # try:
    #     afisha_new(sql)
    # except:
    #     print("???????????????????? ???? ??????????????????")
    await state.finish()

    # time=datetime.time.strptime(data['date']+data['time'],"%d-%m-%Y%H:%M")
