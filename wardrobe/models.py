from pathlib import Path
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .constants import CLOTHING_TYPES, COLORS, STYLES, WEATHERS


def garment_upload_path(instance, filename):
    extension = Path(filename).suffix.lower()
    return f"garments/user_{instance.owner_id}/{uuid.uuid4().hex}{extension}"


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

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("owner", "clothing_type")),
            models.Index(fields=("owner", "style")),
        ]

    def __str__(self):
        return f"{self.name} ({self.clothing_type})"


class Outfit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outfits")
    name = models.CharField(max_length=120, blank=True)
    style = models.CharField(max_length=40, default="Any")
    weather = models.CharField(max_length=10, default="Any")
    garments = models.ManyToManyField(Garment, related_name="outfits")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        if self.owner_id and self.pk:
            invalid = self.garments.exclude(owner_id=self.owner_id).exists()
            if invalid:
                raise ValidationError("Every garment must belong to the outfit owner.")

    @property
    def display_name(self):
        return self.name or f"Outfit from {self.created_at:%b %d, %Y}"

    def __str__(self):
        return self.display_name
