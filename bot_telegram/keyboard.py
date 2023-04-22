from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Кнопки, которые будут на клавиатуре пользователя при обращении к боту.
button_weather = KeyboardButton('/Узнать_погоду')
button_converter = KeyboardButton('/Конвертировать_валюту')
button_animals = KeyboardButton('/Поднять_настроение')

# Клавиатура - меню с выбором из вышеперечисленных кнопок.
keyboard_first_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_first_menu.add(button_weather).insert(button_converter).add(button_animals)


