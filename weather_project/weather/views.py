from django.shortcuts import render
from django.http import JsonResponse
from .services import get_weather, search_city


def home(request):
    context = {}

    if request.method == "POST":
        city = request.POST.get("city")

        if not city:
            context["error"] = "Please enter a city name."
            return render(request, "weather/index.html", context)

        data = get_weather(city)

        if "error" in data:
            context["error"] = "Wrong city name. Please try again."
        else:
            context["weather"] = {
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "temp": data["current"]["temp_c"],
                "feels_like": data["current"]["feelslike_c"],
                "humidity": data["current"]["humidity"],
                "wind": data["current"]["wind_kph"],
                "pressure": data["current"]["pressure_mb"],
                "condition": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"],
            }

    return render(request, "weather/index.html", context)



# 🔥 AJAX endpoint for suggestions
def city_suggestions(request):
    query = request.GET.get("q")

    if not query:
        return JsonResponse([], safe=False)

    results = search_city(query)

    suggestions = [
        f"{city['name']}, {city['country']}" for city in results
    ]

    return JsonResponse(suggestions, safe=False)
