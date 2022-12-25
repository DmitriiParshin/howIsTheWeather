import datetime
from pprint import pprint

import requests
from config import OPEN_WEATHER_TOKEN


def get_weather(city, OPEN_WEATHER_TOKEN):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U0001F327',
        'Mist': 'Туман \U0001F32B',
        'Snow': 'Снег \U0001F328',
        'Drizzle': 'Морось \U0001F327',
        'Thunderstorm': 'Гроза \U0001F329'

    }

    try:
        request = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}'
            f'&lang=ru&appid={OPEN_WEATHER_TOKEN}&units=metric'
        )
        data = request.json()
        pprint(data)

        city = data['name']
        weather = data['weather'][0]['description']
        if weather in code_to_smile:
            smile = code_to_smile[weather]
        else:
            smile = "Посмотри"
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_day = sunset - sunrise

        print(
            f'*** {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")} ***\n'
            f'city: {city}\nweather: {weather}\ncur_weather:{cur_weather}\n'
            f'humidity: {humidity}\npressure :{pressure}\nwind: {wind}\n'
            f'sunrise: {sunrise}\nsunset: {sunset}\nlength_day: {length_day}'
        )

    except Exception as error:
        print(error)
        print("Check name city")


def main():
    city = input('Enter city: ')
    get_weather(city, OPEN_WEATHER_TOKEN)


if __name__ == '__main__':
    main()
