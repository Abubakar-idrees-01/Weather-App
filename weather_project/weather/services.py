import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_forecast(city):
    # Using your preferred WeatherAPI URL
    url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&aqi=no&alerts=no"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return {"error": {"message": "Connection to weather service failed."}}

def search_city(query):
    url = f"https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}"
    response = requests.get(url)
    return response.json()

def get_current_weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    return response.json()  