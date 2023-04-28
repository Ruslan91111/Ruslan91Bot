from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import ID
from create_bot import dp, bot


# Класс состояний. Пункты из основного меню.
class CurrencyStates(StatesGroup):
    # Переменные, куда будут сохраняться ответы пользователя.
    name_of_currency_from = State()
    name_of_currency_to = State()
    sum_of_currency_from_user = State()


# Машина состояний: Вопрос для опроса и 4 варианта ответа.
class FSMAdmin(StatesGroup):
    question = State()
    variant1 = State()
    variant2 = State()
    variant3 = State()
    variant4 = State()


# Начало диалога и загрузки опроса. Создать опрос могу только я. Мой ID в файле config.
async def start_make_poll(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.question.set()
        await message.reply('Введите вопрос для опроса.')


# Ловим вопрос и сохраняем в словарь.
async def save_the_question(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['question'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 1")


# Ловим первый вариант ответа и сохраняем в словарь.
async def save_the_variant1(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['variant1'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 2")


# Ловим второй вариант.
async def save_the_variant2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as poll:
            poll['variant2'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 3")


# Ловим третий вариант.
async def save_the_variant3(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:

        async with state.proxy() as poll:
            poll['variant3'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите вариант ответа 4")


# Ловим четвертый вариант. И посылаем опрос в группу.
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


def register_handlers_poll(dp: Dispatcher):
    dp.register_message_handler(start_make_poll, commands="Создать_опрос", state=None)
    dp.register_message_handler(save_the_question, state=FSMAdmin.question)
    dp.register_message_handler(save_the_variant1, state=FSMAdmin.variant1)
    dp.register_message_handler(save_the_variant2, state=FSMAdmin.variant2)
    dp.register_message_handler(save_the_variant3, state=FSMAdmin.variant3)
    dp.register_message_handler(save_the_variant4, state=FSMAdmin.variant4)

