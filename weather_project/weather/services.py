import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    return response.json()


def search_city(query):
    url = f"https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}"
    response = requests.get(url)
    return response.json()
