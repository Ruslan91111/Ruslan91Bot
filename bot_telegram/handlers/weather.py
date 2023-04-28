from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import dp
from get_by_api import get_the_weather_by_api


class NameOfCityState(StatesGroup):
    name_of_city = State()  # Относится к выводу погоды


# При выборе в меню пункта - "Узнать погоду", сохраняем первое состояние - название города.
async def check_the_weather(message: types.Message):
    await message.answer("Введите город, в котором вы хотели бы узнать погоду.")
    await NameOfCityState.name_of_city.set()


# Работа с предоставлением погоды по городу.
@dp.message_handler(state=NameOfCityState.name_of_city)
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


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(check_the_weather, commands=['Узнать_погоду'])

