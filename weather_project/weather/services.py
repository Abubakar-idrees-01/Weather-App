from decouple import config
import requests
import json

API_KEY = config('WEATHER_API_KEY')

def tcity(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Check if API returned error
        if "error" in data:
            return {"error": True, "message": "Wrong city name!"}

        location = data["location"]
        current = data["current"]

        return {
            "error": False,
            "city": location["name"],
            "region": location["region"],
            "country": location["country"],
            "localtime": location["localtime"],
            "temp_c": current["temp_c"],
            "feelslike_c": current["feelslike_c"],
            "condition_text": current["condition"]["text"],
            "condition_icon": "https:" + current["condition"]["icon"],
            "wind_kph": current["wind_kph"],
            "wind_dir": current["wind_dir"],
            "humidity": current["humidity"],
            "cloud": current["cloud"],
            "precip_mm": current["precip_mm"],
            "pressure_mb": current["pressure_mb"],
            "uv": current["uv"],
            "vis_km": current["vis_km"]
        }

    except requests.exceptions.RequestException:
        return {"error": True, "message": "API request failed!"}
