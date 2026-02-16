from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("suggest/", views.city_suggestions, name="city_suggestions"),
    path("compare/", views.compare_weather, name="compare"),  # comparison page
]
