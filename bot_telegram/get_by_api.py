"""Три функции обращения к API для получения сведений о погоде, курса валют и случайной картинки с котиком. """
import re
import aiohttp
from config import API_WEATHER


async def get_the_weather_by_api(city: str) -> str:
    """ Запрашивает через API данные погоды в определенном городе, возвращает готовый ответ в виде строки."""
    url = f"http://api.openweathermap.org/data/2.5/find?q={city.strip()}&type=like&APPID={API_WEATHER}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            weather_in_city = await response.json()
            print(weather_in_city)
            # Проверяем, что город был введен правильно. Если нет, то ['list'] пустой.
            if weather_in_city['list']:
                # Выбираем нужные нам значения, из которых сформируем возвращаемую строку.
                real_temperature = weather_in_city['list'][0]['main']['temp']
                fills_like_temperature = weather_in_city['list'][0]['main']['feels_like']
                wind = weather_in_city['list'][0]['wind']['speed']
                rain = ', в настоящее время идёт дождь' if weather_in_city['list'][0]['rain'] else ''
                snow = ', в настоящее время идёт снег' if weather_in_city['list'][0]['snow'] else ''

                return(f'В настоящее время в населенном пункте {city} температура воздуха {real_temperature}°C, '
                       f'ощущается как {fills_like_temperature}°C, скорость ветра {wind}м/с{rain}{snow}')

            # Сообщение пользователю, если наименование города было введено неверно.
            else:
                return 'Населенного пункта с указанным названием не найдено.'


async def convert_by_api(currencies_and_sum_from_user: dict) -> str:
    """ Запрашивает через API курс, считаем сумму в функции, возвращает готовый ответ в виде строки."""
    # Формируем нужный url.
    currency_from = re.sub(r"[^A-Z]", '', currencies_and_sum_from_user['currency_from'])
    currency_to = re.sub(r"[^A-Z]", '', currencies_and_sum_from_user['currency_to'])
    url = f"https://api.exchangerate.host/convert?from={currency_from}&to={currency_to}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_information = await response.json()
            # Извлекаем курс.
            rate = float(response_information['info']['rate'])
            # Сумма, введенная пользователем.
            sum_from_user = float(currencies_and_sum_from_user['sum_of_currency'])
            if sum_from_user > 0:
                # Вычисление.
                sum_after_convert = sum_from_user * rate
                # Преобразование к двум цифрам после точки.
                sum_after_convert = float('{:.2f}'.format(sum_after_convert))
                return f"{sum_from_user} {currency_from} равняется {sum_after_convert} {currency_to}. " \
                       f"Курс 1 {currency_from} = {rate} {currency_to}"
            else:
                return "Требуется вводить числа больше 0. Попробуйте еще раз."


# Получить картинку с котиком
async def get_the_cat() -> str:
    """ Запрашивает по API адрес картинки с котиком, возвращает готовый url в виде строки."""
    url = f"https://api.thecatapi.com/v1/images/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_information = await response.json()
            return response_information[0]['url']




