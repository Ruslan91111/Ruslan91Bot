"""Файл - точка входа в приложение"""
import logging
from aiogram import executor, Dispatcher
from create_bot import dp
import client


# Configure logging
logging.basicConfig(level=logging.INFO)

# Регистрируем handlers из модулей.
client.register_handlers_client(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


