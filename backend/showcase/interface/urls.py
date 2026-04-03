from django.urls import path

from showcase.interface import views

urlpatterns = [
    # Health Check
    path("health/", views.health, name="health"),
    # Auth
    path("auth/me/", views.auth_me, name="auth-me"),
    path("auth/register/", views.auth_register, name="auth-register"),
    path("auth/login/", views.auth_login, name="auth-login"),
    path("auth/refresh/", views.auth_refresh, name="auth-refresh"),
    # Dogs
    path("dogs/", views.dogs, name="dogs"),
    path("dogs/<uuid:dog_id>/", views.dog_detail, name="dog-detail"),
    # Breeds
    path("breeds/", views.breeds_list, name="breeds-list"),
]
