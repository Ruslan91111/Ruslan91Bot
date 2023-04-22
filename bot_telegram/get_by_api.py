import aiohttp
import requests
import json
from config import API_WEATHER


async def get_the_weather_by_api(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/find?q={city.strip()}&type=like&APPID={API_WEATHER}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            print(response_text)



# Вариант через requests
# def get_the_weather_by_api(city: str) -> str:
#     url = f"http://api.openweathermap.org/data/2.5/find?q={city.strip()}&type=like&APPID=8537d9ef6386cb97156fd47d832f479c"
#     print(url)
#     response = requests.get(url)
#     x = response.json()
#     print(x)
