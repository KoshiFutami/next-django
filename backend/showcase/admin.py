from django.contrib import admin

from showcase.models import Breed, Dog, OwnerProfile


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname", "user", "created_at")
    search_fields = ("nickname", "user__email", "user__username")


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "sort_order")


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "breed", "created_at")
    list_filter = ("breed",)
