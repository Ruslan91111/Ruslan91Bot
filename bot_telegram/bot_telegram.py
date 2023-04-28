""" Основной файл - точка входа в приложение.

Содержит один handler, приветствующий пользователя и выводящий главное меню,
остальные handlers находятся в отдельном одноименном пакете."""

from aiogram import executor, types
from aiogram.types import KeyboardButton

from keyboard import keyboard_first_menu
from create_bot import dp
from config import ID
# Импорты handlers бота, которые находятся в отдельном пакете.
from handlers.weather import register_handlers_weather
from handlers.currency_convert import register_handlers_currency_convert
from handlers.poll import register_handlers_poll
from handlers.show_a_cat import register_handlers_show_a_cat


# Приветствие, затем вывод первичного меню.
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ В ответ на `/start` or `/help` поприветствовать пользователя, вывести главное меню. """
    # Если мой ID - "Создателя бота", то вывести дополнительную кнопку создать опрос.
    if message.from_user.id == ID:
        await message.answer("Здравствуйте, создатель, чтобы вы хотели?",
                             reply_markup=keyboard_first_menu.insert(KeyboardButton('/Создать_опрос')))
    # Меню для всех пользователей.
    else:
        await message.answer("Здравствуйте, я бот Ruslan91\nниже меню того, что я умею, \n"
                             "выберите подходящий для Вас пункт.", reply_markup=keyboard_first_menu)

# handlers
register_handlers_weather(dp)
register_handlers_currency_convert(dp)
register_handlers_poll(dp)
register_handlers_show_a_cat(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

