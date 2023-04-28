"""Промежуточный файл, в котором создаются объекты Bot и Dispatcher,
  файл нужен, чтобы избежать кольцевания импортов, между bot_telegram.py и файлами с handlers. """
from aiogram import Bot, Dispatcher
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Хранилище временных файлов - оперативная память.
storage = MemoryStorage()

# Инициализация экземпляров бота и диспетчера.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

