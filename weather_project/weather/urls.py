from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("suggest/", views.city_suggestions, name="city_suggestions"),
]
