from django.urls import path

from . import views

app_name = "wardrobe"

# URL patterns for the wardrobe app, mapping URLs to their corresponding view functions.
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("wardrobe/", views.garment_list, name="garment_list"),
    path("wardrobe/add/", views.garment_create, name="garment_create"),
    path("wardrobe/<int:pk>/edit/", views.garment_update, name="garment_update"),
    path("wardrobe/<int:pk>/delete/", views.garment_delete, name="garment_delete"),
    path("generate/", views.generator, name="generator"),
    path("generate/save/", views.save_generated_outfit, name="save_generated_outfit"),
    path("outfits/", views.outfit_list, name="outfit_list"),
    path("outfits/<int:pk>/", views.outfit_detail, name="outfit_detail"),
    path("outfits/<int:pk>/delete/", views.outfit_delete, name="outfit_delete"),
]
