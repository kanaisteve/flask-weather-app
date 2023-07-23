import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv
api_key = os.getenv('API_KEY')

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int

# Please use ISO 3166 country codes.
# accurate way to specify any location
# Geocoding converts any location name into geographical coordinates
# Geocoder onverts city names and zip-codes to geo coordinates and the other way around
def get_geographical_coordinates(city_name, state_code, country_code, API_KEY):
    GEO_CODING_URL = 'http://api.openweathermap.org/geo/1.0/direct'
    res = requests.get(f'{GEO_CODING_URL}?q={city_name},{state_code},{country_code}&appid={API_KEY}').json()

    data = res[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

# Access current weather data for any given geographical cordinates
def get_current_weather(lat, lon, API_KEY):
    request_url = f'{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    res = requests.get(request_url).json()

    data = WeatherData(
        main = res.get('weather')[0].get('main'),
        description=res.get('weather')[0].get('description'),
        icon = res.get('weather')[0].get('icon'),
        temperature = int(res.get('main').get('temp'))
    )

    return data

def get_weather(city_name, state_name, country_name):
    lat, lon = get_geographical_coordinates(city_name, state_name, country_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data


if __name__ == '__main__':
    lat, lon = get_geographical_coordinates('Toronto', 'ON', 'Canada', api_key)
    print(get_current_weather(lat, lon, api_key))