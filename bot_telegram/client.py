""""""

from aiogram import Bot, types, Dispatcher
from create_bot import dp, bot


# Приветственное сообщение-начало работы.
async def send_welcome(message: types.Message):
    """ Поприветствовать пользователя"""
    await message.answer("Здравствуйте, я бот Ruslan91Bot.\nВыберите, пожалуйста нужную функцию.")


# Регистрируем handlers
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
