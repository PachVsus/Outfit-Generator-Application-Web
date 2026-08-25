from django.contrib import admin

from .models import Garment, Outfit


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "clothing_type", "style", "weather", "created_at")
    list_filter = ("clothing_type", "style", "weather")
    search_fields = ("name", "owner__username")


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("display_name", "owner", "style", "weather", "created_at")
    search_fields = ("name", "owner__username")
