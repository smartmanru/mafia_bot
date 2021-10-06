from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram_forms import fields, forms
from loader import dp


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
