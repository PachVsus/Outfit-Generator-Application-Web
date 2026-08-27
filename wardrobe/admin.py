from django.contrib import admin

from .models import Garment, GarmentStyle, Outfit


@admin.register(GarmentStyle)
class GarmentStyleAdmin(admin.ModelAdmin):
    search_fields = ("name",)


## Admin classes for the wardrobe app, customizing the display and search functionality for Garment and Outfit models in the Django admin interface.
@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "clothing_type", "style_names", "weather", "created_at")
    list_filter = ("clothing_type", "styles", "weather")
    search_fields = ("name", "owner__username")
    filter_horizontal = ("styles",)

    @admin.display(description="Styles")
    def style_names(self, garment):
        return ", ".join(garment.styles.values_list("name", flat=True))


## Admin class for the Outfit model, customizing the display and search functionality in the Django admin interface.
@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("display_name", "owner", "style", "weather", "created_at")
    search_fields = ("name", "owner__username")
