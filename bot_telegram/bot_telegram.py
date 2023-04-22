import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN
from keyboard import keyboard_first_menu
from get_by_api import get_the_weather_by_api

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
    await message.reply("Здравствуйте, я бот Ruslan91\nниже меню того, что я умею, \n"
                        "выберите подходящий для Вас пункт.", reply_markup=keyboard_first_menu)


# Класс состояний. Ответы на вопросы из меню.
class AnswersFromUser(StatesGroup):
    first_answer = State()
    additional_answer = State()


@dp.message_handler(commands=['Узнать_погоду'])
async def check_the_weather(message: types.Message):
    await message.answer("Введите город, в котором вы хотели бы узнать погоду.")
    await AnswersFromUser.first_answer.set()


@dp.message_handler(state=AnswersFromUser.first_answer)
async def get_the_weather(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    # Логика - запрашиваем погоду через API.
    city = await state.get_data('city')  # убрать

    # print(city['city'])  # убрать

    # Отправляем город в функцию.
    data =  await get_the_weather_by_api(city['city'])




# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#     await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)