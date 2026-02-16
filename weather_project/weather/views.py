# weather/views.py
from django.shortcuts import render
from .services import tcity

def home(request):
    city = request.GET.get("city", "Gojra")
    weather = tcity(city)

    context = {"weather": weather}
    return render(request, "weather/index.html", context)
