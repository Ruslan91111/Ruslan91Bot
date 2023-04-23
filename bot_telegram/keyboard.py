from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Кнопки, которые будут на клавиатуре в первом меню при обращении к боту.
button_weather = KeyboardButton('/Узнать_погоду')
button_converter = KeyboardButton('/Конвертировать_валюту')
button_animals = KeyboardButton('/Поднять_настроение')

# Клавиатура - меню с выбором из вышеперечисленных кнопок.
keyboard_first_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_first_menu.add(button_weather).insert(button_converter).add(button_animals)


# Кнопки с названием валют.
button_usd = KeyboardButton('$ USD')
button_eur = KeyboardButton('€ EUR')
button_rub = KeyboardButton('₽ RUB')
button_cny = KeyboardButton('¥ CNY')
button_another = KeyboardButton('Другая')

# Клавиатура валют.
keyboard_currency = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_currency.add(button_usd).insert(button_eur).add(button_rub).insert(button_rub).\
    add(button_cny).insert(button_another)




