from django.urls import path
from . import views

urlpatterns = [
    path("", views.weather_home, name="weather_home"),
    path("suggest/", views.city_suggestions, name="city_suggestions"),
    path("compare/", views.compare_weather, name="compare"),  # comparison page
]
