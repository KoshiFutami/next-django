from django.urls import path

from showcase.interface import views

urlpatterns = [
    # Health Check
    path("health/", views.health, name="health"),
    # Dogs
    path("dogs/", views.dogs, name="dogs"),
    path("dogs/<uuid:dog_id>/", views.dog_detail, name="dog-detail"),
    # Breeds
    path("breeds/", views.breeds_list, name="breeds-list"),
]
