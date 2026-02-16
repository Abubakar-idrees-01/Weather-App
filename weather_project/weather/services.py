import requests # This looks at the library we just reinstalled
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_forecast(city):
    # 1. Get coordinates
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_res = requests.get(geo_url).json()
    
    if not geo_res.get('results'):
        return {"error": {"message": "City not found"}}
    
    location = geo_res['results'][0]
    lat, lon = location['latitude'], location['longitude']

    # 2. Get weather data
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,surface_pressure,wind_speed_10m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,temperature_2m_mean&timezone=auto"
    data = requests.get(weather_url).json()

    formatted_data = {
        "location": {"name": location['name'], "country": location.get('country', '')},
        "current": {
            "temp_c": data['current']['temperature_2m'],
            "feelslike_c": data['current']['apparent_temperature'],
            "humidity": data['current']['relative_humidity_2m'],
            "wind_kph": data['current']['wind_speed_10m'],
            "pressure_mb": data['current']['surface_pressure'],
            "condition": {
                "text": "Current", 
                "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png" # Current Icon
            }
        },
        "forecast": {"forecastday": []}
    }

    # Populate 7 days - ADDING THE MISSING ICON HERE
    for i in range(len(data['daily']['time'])):
        formatted_data["forecast"]["forecastday"].append({
            "date": data['daily']['time'][i],
            "day": {
                "maxtemp_c": data['daily']['temperature_2m_max'][i],
                "mintemp_c": data['daily']['temperature_2m_min'][i],
                "avgtemp_c": data['daily']['temperature_2m_mean'][i],
                # CRITICAL FIX: Added the condition dictionary so views.py can find it
                "condition": {
                    "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png" 
                }
            }
        })
    
    return formatted_data

def search_city(query):
    url = f"https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}"
    response = requests.get(url)
    return response.json()

def get_current_weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    return response.json()