from django.urls import path

from showcase.interface import views

urlpatterns = [
    # Health Check
    path("health/", views.health, name="health"),
    path("auth/me/", views.auth_me, name="auth-me"),
    # Dogs
    path("dogs/", views.dogs, name="dogs"),
    path("dogs/<uuid:dog_id>/", views.dog_detail, name="dog-detail"),
    # Breeds
    path("breeds/", views.breeds_list, name="breeds-list"),
]
