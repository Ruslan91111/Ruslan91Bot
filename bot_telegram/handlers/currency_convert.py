from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from create_bot import dp
from get_by_api import convert_by_api
from keyboard import keyboard_currency, keyboard_first_menu




# Класс состояний. Пункты из основного меню.
class CurrencyStates(StatesGroup):
    # Переменные, куда будут сохраняться ответы пользователя.
    name_of_currency_from = State()
    name_of_currency_to = State()
    sum_of_currency_from_user = State()


# При выборе в меню пункта - "Конвертировать_валюту".
async def currency_from(message: types.Message):
    await message.answer("Выберите валюту, которую хотите конвертировать.\nЕсли на клавиатуре "
                         "нет желаемой валюты, введите название валюты самостоятельно\n"
                         "Если передумали, введите команду 'Отмена'.", reply_markup=keyboard_currency)
    await CurrencyStates.name_of_currency_from.set()


# Получаем валюту, которую будем конвертировать.
async def currency_from_state(message: types.Message, state: FSMContext):
    await state.update_data(currency_from=message.text)
    await message.answer("Отлично! Теперь введите валюту, в которую необходимо конвертировать.",
                         reply_markup=keyboard_currency)
    await CurrencyStates.next()  # либо же AnswersFromUser.name_of_currency_to.set()


# Вторая валюта. Получаем валюту, в которую будем конвертировать.
async def currency_to(message: types.Message, state: FSMContext):
    await state.update_data(currency_to=message.text)
    await message.answer("Отлично! Теперь введите сумму, которую вы хотите конвертировать.",)
    await CurrencyStates.next()  # либо же AnswersFromUser.sum_of_currency_from_user.set()


# Получаем сумму валюты, которую будем конвертировать.
async def currency_to_state(message: types.Message, state: FSMContext):
    await state.update_data(sum_of_currency=message.text)
    await CurrencyStates.next()  # либо же AnswersFromUser.sum_of_currency_from_user.set()
    # Логика. Извлекаем данные из состояния: два наименования валюты и сумму.
    currencies_and_sum_from_user = await state.get_data()
    # Вызываем функцию, которая обратится по API к сайту с курсами валют, посчитает и вернет строку с готовым ответом.
    answer_to_user = await convert_by_api(currencies_and_sum_from_user)
    await message.answer(answer_to_user, reply_markup=keyboard_first_menu)
    # Завершили состояние.
    await state.finish()


# Выход из машины состояний.
@dp.message_handler(commands="отмена", state="*", )
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отменено.', reply_markup=keyboard_first_menu)


def register_handlers_currency_convert(dp: Dispatcher):
    dp.register_message_handler(currency_from, commands=['Конвертировать_валюту'])
    dp.register_message_handler(currency_from_state, state=CurrencyStates.name_of_currency_from)
    dp.register_message_handler(currency_to, state=CurrencyStates.name_of_currency_to)
    dp.register_message_handler(currency_to_state, state=CurrencyStates.sum_of_currency_from_user)

