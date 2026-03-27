from django.urls import path

from showcase.interface import views

urlpatterns = [
    path("health/", views.health, name="health"),
]
