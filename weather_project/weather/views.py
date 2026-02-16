from django.shortcuts import render
from django.http import JsonResponse
from .services import get_weather_forecast, search_city, get_current_weather
from datetime import datetime

from datetime import datetime

def home(request):
    context = {}
    if request.method == "POST":
        city = request.POST.get("city")
        data = get_weather_forecast(city) # Your existing API helper

        if not data or "error" in data:
            context["error"] = "City not found."
            return render(request, "weather/index.html", context)

        # Current Weather
        context["weather"] = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temp": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "feels_like": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "wind": data["current"]["wind_kph"],
            "pressure": data["current"]["pressure_mb"],
        }

        chart_labels = []
        chart_values = []
        forecast_cards = []

        for day in data["forecast"]["forecastday"]:
            # 1. Fill Daily Cards (Bottom row)
            date_dt = datetime.strptime(day["date"], "%Y-%m-%d")
            forecast_cards.append({
                "date": date_dt.strftime("%a"),
                "max_temp": day["day"]["maxtemp_c"],
                "min_temp": day["day"]["mintemp_c"],
                "icon": day["day"]["condition"]["icon"],
                "condition": day["day"]["condition"]["text"],
            })

            # 2. Extract Hourly data (00:00, 06:00, 12:00, 18:00)
            for h_idx in [0, 6, 12, 18]:
                hour = day["hour"][h_idx]
                time_str = datetime.strptime(hour["time"], "%Y-%m-%d %H:%M").strftime("%a %I%p")
                chart_labels.append(time_str)
                chart_values.append(hour["temp_c"])

        context["forecast"] = forecast_cards
        context["chart_labels"] = chart_labels
        context["chart_values"] = chart_values

    return render(request, "weather/index.html", context)

# Compare logic (also uses WeatherAPI icon structure)
def compare_weather(request):
    context = {}
    if request.method == "POST":
        city1_name = request.POST.get("city1")
        city2_name = request.POST.get("city2")

        data1 = get_current_weather(city1_name)
        data2 = get_current_weather(city2_name)

        if "error" in data1 or "error" in data2:
            context["error"] = "One or both cities could not be found."
            return render(request, "weather/compare.html", context)

        for i, data in enumerate([data1, data2], 1):
            context[f"city{i}"] = {
                "name": data["location"]["name"],
                "temp": data["current"]["temp_c"],
                "icon": data["current"]["condition"]["icon"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "wind": data["current"]["wind_kph"],
            }
        
        context["temp_difference"] = round(context["city1"]["temp"] - context["city2"]["temp"], 1)

    return render(request, "weather/compare.html", context)

def city_suggestions(request):
    query = request.GET.get("q")
    if not query: return JsonResponse([], safe=False)
    try:
        results = search_city(query)
        suggestions = [f"{c['name']}, {c['country']}" for c in results]
        return JsonResponse(suggestions, safe=False)
    except:
        return JsonResponse([], safe=False)