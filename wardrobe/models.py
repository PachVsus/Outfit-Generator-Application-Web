from pathlib import Path
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .constants import CLOTHING_TYPES, COLORS, STYLES, WEATHERS

# Utility function to generate a unique upload path for garment images based on the owner's ID and a UUID.
def garment_upload_path(instance, filename):
    extension = Path(filename).suffix.lower()
    return f"garments/user_{instance.owner_id}/{uuid.uuid4().hex}{extension}"

# Garment model representing individual clothing items in the user's wardrobe.
class Garment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="garments")
    name = models.CharField(max_length=120)
    clothing_type = models.CharField(max_length=20, choices=CLOTHING_TYPES)
    main_color = models.CharField(max_length=30, choices=[(color, color) for color in COLORS])
    secondary_color = models.CharField(max_length=30, choices=[(color, color) for color in COLORS], blank=True)
    style = models.CharField(max_length=40, choices=[(style, style) for style in STYLES])
    weather = models.CharField(max_length=10, choices=[(weather, weather) for weather in WEATHERS], default="Any")
    image = models.ImageField(upload_to=garment_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Meta class to define ordering and indexes for the Garment model.
    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("owner", "clothing_type")),
            models.Index(fields=("owner", "style")),
        ]

    # String representation of the Garment model, returning the name and clothing type.
    def __str__(self):
        return f"{self.name} ({self.clothing_type})"

# Outfit model representing a collection of garments that make up an outfit.
class Outfit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outfits")
    name = models.CharField(max_length=120, blank=True)
    style = models.CharField(max_length=40, default="Any")
    weather = models.CharField(max_length=10, default="Any")
    garments = models.ManyToManyField(Garment, related_name="outfits")
    created_at = models.DateTimeField(auto_now_add=True)

    # Meta class to define ordering for the Outfit model.
    class Meta:
        ordering = ("-created_at",)

    # Clean method to ensure that all garments in the outfit belong to the same owner as the outfit itself.
    def clean(self):
        if self.owner_id and self.pk:
            invalid = self.garments.exclude(owner_id=self.owner_id).exists()
            if invalid:
                raise ValidationError("Every garment must belong to the outfit owner.")

    # Property to display the outfit's name or a default name based on the creation date if no name is provided.
    @property
    def display_name(self):
        return self.name or f"Outfit from {self.created_at:%b %d, %Y}"

    # String representation of the Outfit model, returning the display name.
    def __str__(self):
        return self.display_name
