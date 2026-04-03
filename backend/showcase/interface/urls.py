from django.urls import path

from showcase.interface import views

urlpatterns = [
    # Health Check
    path("health/", views.health, name="health"),
    # Dogs
    path("dogs/", views.dogs, name="dogs"),
    # Breeds
    path("breeds/", views.breeds_list, name="breeds-list"),
]
