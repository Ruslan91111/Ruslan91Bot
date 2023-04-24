""" Основной файл - точка входа в приложение. """
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import keyboard_first_menu, keyboard_currency

from config import API_TOKEN, ID
from get_by_api import get_the_weather_by_api, convert_by_api, get_the_cat


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


# Класс состояний. Пункты из основного меню.
class AnswersFromUser(StatesGroup):
    name_of_city = State()  # Относится к выводу погоды
    # Переменные, связанные с работой конвертера.
    name_of_currency_from = State()
    name_of_currency_to = State()
    sum_of_currency_from_user = State()


# При выборе в меню пункта - "Узнать погоду", сохраняем первое состояние - название города.
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
    # Отправляем город в функцию, которая обратится по API сайта погоды, получаем готовую строку - ответ.
    weather_in_the_city = await get_the_weather_by_api(city['city'])
    # Выводим.
    await message.answer(weather_in_the_city)
    await message.answer("Для просмотра информации о другом городе выберите '/Узнать погоду'")
    await state.finish()


# При выборе в меню пункта - "Конвертировать_валюту".
@dp.message_handler(commands=['Конвертировать_валюту'])
async def currency_from(message: types.Message):
    await message.answer("Выберите валюту, которую хотите конвертировать.\nЕсли на клавиатуре "
                         "нет желаемой валюты, введите название валюты самостоятельно",
                         reply_markup=keyboard_currency)
    await AnswersFromUser.name_of_currency_from.set()


# Получаем валюту, которую будем конвертировать.
@dp.message_handler(state=AnswersFromUser.name_of_currency_from)
async def currency_from_state(message: types.Message, state: FSMContext):
    await state.update_data(currency_from=message.text)
    await message.answer("Отлично! Теперь введите валюту, в которую необходимо конвертировать.",
                         reply_markup=keyboard_currency)
    await AnswersFromUser.next()  # либо же AnswersFromUser.name_of_currency_to.set()


# Вторая валюта. Получаем валюту, в которую будем конвертировать.
@dp.message_handler(state=AnswersFromUser.name_of_currency_to)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(currency_to=message.text)
    await message.answer("Отлично! Теперь введите сумму, которую вы хотите конвертировать.",)
    await AnswersFromUser.next()  # либо же AnswersFromUser.sum_of_currency_from_user.set()


# Получаем сумму валюты, которую будем конвертировать.
@dp.message_handler(state=AnswersFromUser.sum_of_currency_from_user)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(sum_of_currency=message.text)
    await AnswersFromUser.next()  # либо же AnswersFromUser.sum_of_currency_from_user.set()
    # Логика. Извлекаем данные из состояния: два наименования валюты и сумму.
    currencies_and_sum_from_user = await state.get_data()
    # Вызываем функцию, которая обратится по API к сайту с курсами валют, посчитает и вернет строку с готовым ответом.
    answer_to_user = await convert_by_api(currencies_and_sum_from_user)
    await message.answer(answer_to_user, reply_markup=keyboard_first_menu)
    # Завершили состояние.
    await state.finish()


# При выборе в меню пункта - "Показать_милого_котенка"
@dp.message_handler(commands=['Показать_милого_котенка'])
async def show_the_cat(message: types.Message):
    """ Вывести случайную картинку с котиком"""
    await bot.send_photo(message.from_user.id, await get_the_cat())


# Машина состояний: Вопрос для опроса и 4 варианта ответа.
class FSMAdmin(StatesGroup):
    question = State()
    variant1 = State()
    variant2 = State()
    variant3 = State()
    variant4 = State()


# Начало диалога и загрузки опроса. Создать опрос могу только я. Мой ID в файле config.
@dp.message_handler(commands="Создать_опрос", state=None)
async def start_make_poll(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.question.set()
        await message.reply('Введите вопрос для опроса.')


# Ловим вопрос и сохраняем в словарь.
@dp.message_handler(state=FSMAdmin.question)
async def save_the_question(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['question'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 1")


# Ловим первый вариант ответа и сохраняем в словарь.
@dp.message_handler(state=FSMAdmin.variant1)
async def save_the_variant1(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['variant1'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 2")


# Ловим второй вариант.
@dp.message_handler(state=FSMAdmin.variant2)
async def save_the_variant2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['variant2'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 3")


# Ловим третий вариант.
@dp.message_handler(state=FSMAdmin.variant3)
async def save_the_variant3(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:

        async with state.proxy() as poll:
            poll['variant3'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 4")


# Ловим четвертый вариант. И посылаем опрос в группу.
@dp.message_handler(state=FSMAdmin.variant4)
async def save_the_variant4(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['variant4'] = message.text
            await FSMAdmin.next()
            await message.answer("Ввод закончен.")

            # Окончание внесения - посылаем опрос в групповой чат, chat_id прописал конкретный.
            await bot.send_poll(chat_id=-989642232, question=poll['question'],
                                options=[poll['variant1'], poll['variant2'], poll['variant3'], poll['variant4']])

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

