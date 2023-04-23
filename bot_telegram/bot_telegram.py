""" Основной файл - точка входа в приложение. """
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN
from keyboard import keyboard_first_menu, keyboard_currency
from get_by_api import get_the_weather_by_api, convert_by_api
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
# Хранилище временных файлов - оперативная память.
storage = MemoryStorage()

# Инициализация бота и диспетчера.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# Приветствие + вывод первичного меню.
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ В ответ на `/start` or `/help` поприветствовать пользователя, вывести меню. """
    await message.answer("Здравствуйте, я бот Ruslan91\nниже меню того, что я умею, \n"
                         "выберите подходящий для Вас пункт.", reply_markup=keyboard_first_menu)


# Класс состояний. Ответы пользователя на вопросы.
class AnswersFromUser(StatesGroup):
    name_of_city = State()
    name_of_currency_from = State()
    name_of_currency_to = State()
    sum_of_currency_from_user = State()


# При выборе в меню пункта - "Узнать погоду"
@dp.message_handler(commands=['Узнать_погоду'])
async def check_the_weather(message: types.Message):
    await message.answer("Введите город, в котором вы хотели бы узнать погоду.")
    await AnswersFromUser.name_of_city.set()


# Работа с предоставлением погоды по городу.
@dp.message_handler(state=AnswersFromUser.name_of_city)
async def get_the_weather(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    # Определяем город, по которому ищем погоду.
    city = await state.get_data('city')
    # Отправляем город в функцию и получаем готовую строку - ответ.
    weather_in_the_city = await get_the_weather_by_api(city['city'])
    await message.answer(weather_in_the_city)
    await message.answer("Для просмотра информации о другом городе выберите '/Узнать погоду'")
    await state.finish()


# При выборе в меню пункта - "Конвертировать_валюту"
@dp.message_handler(commands=['Конвертировать_валюту'])
async def currency_from(message: types.Message):
    await message.answer("Выберите валюту, которую хотите конвертировать.\nЕсли на клавиатуре "
                         "нет желаемой валюты, введите название валюты самостоятельно",
                         reply_markup=keyboard_currency)
    await AnswersFromUser.name_of_currency_from.set()


# Состояние первой валюты.
@dp.message_handler(state=AnswersFromUser.name_of_currency_from)
async def currency_from_state(message: types.Message, state: FSMContext):
    await state.update_data(currency_from=message.text)
    await message.answer("Отлично! Теперь введите валюту, в которую необходимо конвертировать.",
                         reply_markup=keyboard_currency)
    await AnswersFromUser.next()  # либо же AnswersFromUser.name_of_currency_to.set()


# Состояние второй валюты.
@dp.message_handler(state=AnswersFromUser.name_of_currency_to)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(currency_to=message.text)
    await message.answer("Отлично! Теперь введите сумму, которую вы хотите конвертировать.",)
    await AnswersFromUser.next()  # либо же AnswersFromUser.sum_of_currency_from_user.set()


# Состояние суммы валюты.
@dp.message_handler(state=AnswersFromUser.sum_of_currency_from_user)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(sum_of_currency=message.text)
    await AnswersFromUser.next()  # либо же AnswersFromUser.sum_of_currency_from_user.set()
    # Логика. Извлекаем данные из состояния
    currencies_and_sum_from_user = await state.get_data()
    # Вызываем функцию - идем к API.
    answer_to_user = await convert_by_api(currencies_and_sum_from_user)
    await message.answer(answer_to_user, reply_markup=keyboard_first_menu)
    await state.finish()







# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#     await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)