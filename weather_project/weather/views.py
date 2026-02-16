from django.shortcuts import render
from django.http import JsonResponse
from .services import get_weather_forecast, search_city, get_current_weather
from datetime import datetime

from datetime import datetime

from django.shortcuts import render
from datetime import datetime

from django.shortcuts import render
from datetime import datetime

def home(request):
    context = {}
    
    if request.method == "POST":
        city = request.POST.get("city")
        data = get_weather_forecast(city) 

        if not data or "error" in data:
            context["error"] = data.get("error", {}).get("message", "City not found.")
            return render(request, "weather/index.html", context)

        # 1. Extract Current Weather
        current = data.get("current", {})
        location = data.get("location", {})
        
        # Safely drill down to the icon
        curr_cond = current.get("condition", {})
        curr_icon = curr_cond.get("icon", "")

        context["weather"] = {
            "city": location.get("name"),
            "country": location.get("country"),
            "temp": current.get("temp_c"),
            "feels_like": current.get("feelslike_c"),
            "humidity": current.get("humidity"),
            "wind": current.get("wind_kph"),
            "pressure": current.get("pressure_mb"),
            "condition": curr_cond.get("text"),
            "icon": curr_icon, 
        }

        # 2. Extract Forecast
        forecast_list = []
        # WeatherAPI returns forecast inside 'forecast' -> 'forecastday'
        raw_forecast = data.get("forecast", {}).get("forecastday", [])

        for day in raw_forecast:
            # Date formatting for Chart
            date_str = day.get("date")
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%a') 
            except:
                formatted_date = date_str

            # Drilling down to the day's specific condition
            day_obj = day.get("day", {})
            condition_obj = day_obj.get("condition", {})
            icon_url = condition_obj.get("icon", "")

            # DEBUG: Uncomment the line below to see icons in your terminal
            # print(f"Date: {formatted_date} | Icon: {icon_url}")

            forecast_list.append({
                "date": formatted_date,
                "avg_temp": day_obj.get("avgtemp_c"),
                "max_temp": day_obj.get("maxtemp_c"),
                "min_temp": day_obj.get("mintemp_c"),
                "icon": icon_url, 
            })
        
        context["forecast"] = forecast_list

    return render(request, "weather/index.html", context)

def compare_weather(request):
    context = {}
    
    if request.method == "POST":
        city1_name = request.POST.get("city1")
        city2_name = request.POST.get("city2")

        if not city1_name or not city2_name:
            context["error"] = "Please enter both city names."
            return render(request, "weather/compare.html", context)

        data1 = get_current_weather(city1_name)
        data2 = get_current_weather(city2_name)

        # Safety check for comparison data
        if "error" in data1 or "error" in data2:
            context["error"] = "One or both cities could not be found."
            return render(request, "weather/compare.html", context)

        # Process City 1
        context["city1"] = {
            "name": data1["location"]["name"],
            "country": data1["location"]["country"],
            "temp": data1["current"]["temp_c"],
            "feels": data1["current"]["feelslike_c"],
            "humidity": data1["current"]["humidity"],
            "wind": data1["current"]["wind_kph"],
            "pressure": data1["current"]["pressure_mb"],
            "condition": data1["current"]["condition"]["text"],
            "icon": data1["current"]["condition"]["icon"],
        }

        # Process City 2
        context["city2"] = {
            "name": data2["location"]["name"],
            "country": data2["location"]["country"],
            "temp": data2["current"]["temp_c"],
            "feels": data2["current"]["feelslike_c"],
            "humidity": data2["current"]["humidity"],
            "wind": data2["current"]["wind_kph"],
            "pressure": data2["current"]["pressure_mb"],
            "condition": data2["current"]["condition"]["text"],
            "icon": data2["current"]["condition"]["icon"],
        }

        # Calculate difference
        diff = context["city1"]["temp"] - context["city2"]["temp"]
        context["temp_difference"] = round(diff, 1)

    return render(request, "weather/compare.html", context)


def city_suggestions(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse([], safe=False)
    
    try:
        results = search_city(query)
        suggestions = [f"{city['name']}, {city['country']}" for city in results]
        return JsonResponse(suggestions, safe=False)
    except:
        return JsonResponse([], safe=False)