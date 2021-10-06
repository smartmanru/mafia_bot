import asyncio
from re import M
from typing import Any

from aiogram import Bot, Dispatcher, filters, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.utils import executor
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (Back, Button, Cancel, Group, Next, Row,
                                        Start)
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_forms import fields, forms
from loguru import logger

# import filters
# import handlers
import middlewares
import utils
from data import config
from keyboards.default.main_keyboard import keyboard
from loader import bot, dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


# from handlers.users.wind import prew_click,  next_click, MySG

async def on_startup(dispatcher:Dispatcher):
    # Устанавливаем дефолтные команды
    DialogRegistry(dispatcher)
    await set_default_commands(dispatcher)
    # await utils.start()
    await on_startup_notify(dispatcher)
class MySG(StatesGroup):
    input = State()
    confirm = State()
async def prew_click(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Going on!")
async def next_click(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Running!")

async def main():
    utils.setup_logger("DEBUG", ["sqlalchemy.engine", "aiogram.bot.api"])
    storage = MemoryStorage()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    registry = DialogRegistry(dp)
    middlewares.setup(dp)
    filters.setup(dp)
    # handlers.users.setup(dp)
    registry.register_start_handler(MySG.input)  # resets stack and start dialogs on /start command
    registry.register(prew_click)
    registry.register(next_click)

    await dp.start_polling()


# from aiogram.dispatcher.filters.builtin import CommandStart


async def bot_start(message: types.Message):
    # user_channel_status = await  ('-1001288333015', message.from_user.id)
    user_channel_status= await bot.get_chat_member(chat_id=config.CHANNEL_ID,user_id=message.from_user.id)

    if user_channel_status["status"] != 'left':
        logger.info('c каналом все гуд')
        await message.answer(f"Привет, {message.from_user.full_name}!")
        key=await keyboard([["Правила"],["Афиша","Рейтинг"]])
        await message.answer(
        "Test",
        reply_markup=key)
        
    else:
        channel=await bot.get_chat(config.CHANNEL_ID)
        c_t=channel.title
        c_il=channel.invite_link
        # logger.info(channel)
        await message.answer(f"{message.from_user.full_name}, у тебя нету подписки на канал "+c_t+" Чтобы подписаться перейди по ссылке "+c_il+"\n \nКак подпишешься - жми снова /start")




def setup(dp: Dispatcher):
    dp.register_message_handler(help.bot_help, filters.CommandHelp())
    dp.register_message_handler(bot_start, filters.CommandStart())
    dp.register_message_handler(settings , filters.CommandSettings())
   
   
class MySG(StatesGroup):
    main = State()

main_window = Window(
    Const("Hello, unknown person"),  # just a constant text
    Button(Const("Useless button"), id="nothing"),  # button with text and id
    state=MySG.main,  # state is used to identify window between dialogs
)
dialog = Dialog(main_window)


# async def get_data(**kwargs):
#     return {
#         "name": "Tishka17",
#     }
# dialog = Dialog(
#     Window(
#         Format("Hello, {name}!"),
#         Button(Const("Useless button"), id="nothing"),
#         state=MySG.main,
#         getter=get_data,  # here we set our data getter
#     )
# )

# async def go_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
#     await c.message.answer("Going on!")


# async def run_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
#     await c.message.answer("Running!")


# row = Row(
#     Button(Const("Go"), id="go", on_click=go_clicked),
#     Button(Const("Run"), id="run", on_click=run_clicked),
#     Button(Const("Fly"), id="fly"),
# )






# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Эхо без состояния."
                         f"Сообщение:\n"
                         f"{message.text}")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")


class UserForm(forms.Form):
    LANGUAGE_CHOICES = ('English', 'Russian', 'Chinese')
    LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*[
        KeyboardButton(label) for label in LANGUAGE_CHOICES
    ])

    name = fields.StringField('Name')
    language = fields.ChoicesField('Language', LANGUAGE_CHOICES, reply_keyboard=LANGUAGE_KEYBOARD)
    email = fields.EmailField('Email', validation_error_message='Wrong email format!')

async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))

storage = MemoryStorage()
# bot = Bot(token='BOT TOKEN HERE')
# dp = Dispatcher(bot, storage=storage)
# registry = DialogRegistry(dp)




# main_window = Window(
#     Const("Hello, unknown person"),
#     Button(Const("Useless button"), id="nothing"),
#     # state=MySG.main,
# )


raw=Row(
    Button(Const("⏮"), id='Prev',on_click=prew_click),
    Button(Const("✅"), id='Ok'),
    Button(Const("⏭"), id='Next', on_click=next_click)
)


# wind=Window(raw,state=MySG.input)
# dialog = Dialog(wind)
# dial.register(dialog)

async def settings(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["name"] = m.text
    await manager.current_context()
    await dialog.next(manager)
name_dialog = Dialog(
    Window(
        raw,
        MessageInput(str(settings)),
        state=MySG.input,
        getter=MySG.confirm
    )
)


































'''
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
'''


storage = MemoryStorage()
# bot = Bot(token='BOT TOKEN HERE')
# dp = Dispatcher(bot, storage=storage)
# registry = DialogRegistry(dp)




# main_window = Window(
#     Const("Hello, unknown person"),
#     Button(Const("Useless button"), id="nothing"),
#     # state=MySG.main,
# )


raw=Row(
    Button(Const("⏮"), id='Prev',on_click=prew_click),
    Button(Const("✅"), id='Ok'),
    Button(Const("⏭"), id='Next', on_click=next_click)
)


# wind=Window(raw,state=MySG.input)
# dialog = Dialog(wind)
# dial.register(dialog)

async def settings(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["name"] = m.text
    await manager.current_context()
    await dialog.next(manager)
name_dialog = Dialog(
    Window(
        raw,
        MessageInput(str(settings)),
        state=MySG.input,
        getter=MySG.confirm
    )
)











if __name__ == '__main__':

    asyncio.run(main())

#     executor.start_polling(dp, on_startup=on_startup,skip_updates=False)

# bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
