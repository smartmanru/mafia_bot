from aiogram import types
from aiogram.dispatcher import FSMContext
from utils import logger

from loader import dp
from aiogram.dispatcher.filters.state import State


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
async def bot_echo(m: types.Message):
    logger.info(str(m.Text)+str(state))

# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)


async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
