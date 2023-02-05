import datetime
import json
import os

import requests
import aioredis

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv


load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
URL = os.getenv("URL")
OPEN_WEATHER_TOKEN = os.getenv("OPEN_WEATHER_TOKEN")

bot = Bot(token=TG_BOT_TOKEN)
dispatcher = Dispatcher(bot)
redis_client = aioredis.Redis()


@dispatcher.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет, в каком городе тебе надо узнать погоду?")


@dispatcher.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U0001F327",
        "Mist": "Туман \U0001F32B",
        "Snow": "Снег \U0001F328",
        "Drizzle": "Морось \U0001F327",
        "Thunderstorm": "Гроза \U0001F329",
    }

    try:
        cashe_value = await redis_client.get(message.text)
        if not cashe_value:
            request = requests.get(
                f"{URL}?q={message.text}&lang=ru&appid={OPEN_WEATHER_TOKEN}"
                f"&units=metric"
            )
            data = request.json()
        else:
            data = json.loads(cashe_value)
            await redis_client.set(message.text, json.dumps(data))
        await redis_client.close()
        city = data["name"]
        weather = data["weather"][0]["main"]
        if weather in code_to_smile:
            smile = code_to_smile[weather]
        else:
            smile = "Посмотри в окно, не пойму, что там за погода!"
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_day = sunset - sunrise

        await message.reply(
            f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}***\n"
            f"Погода в городе: {city}\nТемпература: {temp}°C {smile}\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\n"
            f"Ветер: {wind} м/с\n"
            f"Восход солнца: {sunrise.strftime('%H:%M:%S')}\n"
            f"Закат солнца: {sunset.strftime('%H:%M:%S')}\n"
            f"Продолжительность дня: {length_day}\n"
        )
    except Exception as error:
        print(error)
        await message.reply("\U00002620 Проверьте название города! \U00002620")


if __name__ == "__main__":
    executor.start_polling(dispatcher)
