from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (Back, Button, Cancel, Group, Next, Row,
                                        Start)
from aiogram_dialog.widgets.text import Const, Format, Multi

storage = MemoryStorage()
# bot = Bot(token='BOT TOKEN HERE')
# dp = Dispatcher(bot, storage=storage)
# registry = DialogRegistry(dp)


class MySG(StatesGroup):
    input = State()
    confirm = State()

# main_window = Window(
#     Const("Hello, unknown person"),
#     Button(Const("Useless button"), id="nothing"),
#     # state=MySG.main,
# )

async def prew_click(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Going on!")
async def next_click(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Running!")
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
