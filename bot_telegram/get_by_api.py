import aiohttp
import requests
import json
from config import API_WEATHER


async def get_the_weather_by_api(city: str) -> str:
    """ Запрашивает через API данные погоды в определенном городе, возвращает готовый ответ в виде строки."""
    url = f"http://api.openweathermap.org/data/2.5/find?q={city.strip()}&type=like&APPID={API_WEATHER}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            # Преобразовываем в словарь.
            weather_in_city = json.loads(response_text)
            # Выбираем нужные нам значения, из которых сформируем возвращаемую строку.
            real_temperature = weather_in_city['list'][0]['main']['temp']
            fills_like_temperature = weather_in_city['list'][0]['main']['feels_like']
            wind = weather_in_city['list'][0]['wind']['speed']
            rain = ', в настоящее время идёт дождь' if weather_in_city['list'][0]['rain'] else ''
            snow = ', в настоящее время идёт снег' if weather_in_city['list'][0]['snow'] else ''

            return(f'В настоящее время в населенном пункте {city} температура воздуха {real_temperature}°C, '
                   f'ощущается как {fills_like_temperature}°C, скорость ветра {wind}м/с{rain}{snow}')


