"""Промежуточный файл, в котором создаются объекты Bot и Dispatcher,
  файл нужен, чтобы избежать кольцевания импортов, между bot_telegram.py и файлами с handlers. """
from aiogram import Bot, Dispatcher, executor, types
import logging
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


