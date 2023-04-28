import types

from aiogram import Dispatcher

from create_bot import bot, dp
from get_by_api import get_the_cat


# При выборе в меню пункта - "Показать_милого_котенка"
async def show_a_cat(message):
    """ Вывести случайную картинку с котиком"""
    await bot.send_photo(message.from_user.id, await get_the_cat())


def register_handlers_show_a_cat(dp: Dispatcher):
    dp.register_message_handler(show_a_cat, commands="Показать_милого_котенка", state=None)
