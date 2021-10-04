
from re import M
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from loader import bot



a=[]
async def settings(msg: Message, state: FSMContext):
    await msg.answer('Введите Фамилию Имя')
    await state.set_state('ФИО')

async def fio(msg: Message, state: FSMContext):
    await state.finish()
    fio=msg.text
    a.append(fio)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)

    await msg.answer('Введите Город')
    await state.set_state('Город')

async def city(msg: Message, state: FSMContext):
    await state.finish()
    city=msg.text
    a.append(city)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await msg.answer('Введите ваш возраст')
    await state.set_state('возраст')

async def age(msg: Message, state: FSMContext):
    await state.finish()
    age=msg.text
    a.append(age)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await msg.answer('Введите Ник для мафии')
    await state.set_state('nick')

async def nick(msg: Message, state: FSMContext):
    await state.finish()
    mf_nn=msg.text
    a.append(mf_nn)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await msg.answer('Введите Вашу профессию')
    await state.set_state('prof')

async def prof(msg: Message, state: FSMContext):
    await state.finish()
    proof=msg.text
    a.append(proof)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await msg.answer('Ваш ежемесячный доход от ')
    await state.set_state('dohod')

async def dohod(msg: Message, state: FSMContext):
    await state.finish()
    dohod=msg.text
    a.append(dohod)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
    await msg.answer('ВВедите ваш номер телефона',reply_markup=markup_request)
    await state.set_state('ph_num')

async def ph_num(msg:Message, state: FSMContext):
    await state.finish()
    if msg.content_type=='contact':
        ph_num=msg.contact.phone_number
    else:
        ph_num=msg.text
    a.append(ph_num)
    # logger.info(a)
    inline_btn_1 = InlineKeyboardButton("🖌Изменить🖌", callback_data='btn1')
    inline_btn_2 = InlineKeyboardButton("☑️Все Ок☑️",callback_data='btn2')
    inline_btn_3 = InlineKeyboardButton("❌Отменить❌",callback_data='cancel')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1,inline_btn_2)
    await msg.answer("Проверьте ваши данные: \nФИО: "+a[0]+"\nГород: "+a[1]+"\nВозраст: "+a[2]+"\nНикнейм для мафии: "+a[3]+"\nПрофессия: "+a[4]+"\nДоход От "+a[5]+"\nНомер телефона: "+a[6]+"\n \nВсе верно?" ,reply_markup=inline_kb1)



async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code==0:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
        InlineKeyboardMarkup().row()




async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))
