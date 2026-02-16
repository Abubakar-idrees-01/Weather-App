from django.shortcuts import render
from django.http import JsonResponse
from .services import get_weather_forecast, search_city, get_current_weather
from datetime import datetime

def home(request):
    context = {}
    
    if request.method == "POST":
        city = request.POST.get("city")
        data = get_weather_forecast(city) 

        # Check for API errors
        if not data or "error" in data:
            context["error"] = data.get("error", {}).get("message", "City not found.")
            return render(request, "weather/index.html", context)

        # 1. Process Current Weather
        current = data.get("current", {})
        location = data.get("location", {})
        curr_cond = current.get("condition", {})

        context["weather"] = {
            "city": location.get("name"),
            "country": location.get("country"),
            "temp": current.get("temp_c"),
            "feels_like": current.get("feelslike_c"),
            "humidity": current.get("humidity"),
            "wind": current.get("wind_kph"),
            "pressure": current.get("pressure_mb"),
            "condition": curr_cond.get("text"), # e.g., "Partly Cloudy"
            "icon": curr_cond.get("icon"),     # e.g., "//cdn.../116.png"
        }

        # 2. Process 7-Day Forecast
        forecast_list = []
        raw_forecast = data.get("forecast", {}).get("forecastday", [])

        for day in raw_forecast:
            # Format date for display (e.g., '2026-02-16' -> 'Mon')
            date_str = day.get("date")
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%a') 
            except:
                formatted_date = date_str

            # Drill into 'day' object for daily metrics
            day_metrics = day.get("day", {})
            day_cond = day_metrics.get("condition", {})

            forecast_list.append({
                "date": formatted_date,
                "avg_temp": day_metrics.get("avgtemp_c"),
                "max_temp": day_metrics.get("maxtemp_c"),
                "min_temp": day_metrics.get("mintemp_c"),
                "icon": day_cond.get("icon"), # Unique icon for each day!
                "condition": day_cond.get("text"),
            })
        
        context["forecast"] = forecast_list

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