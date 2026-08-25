from django.apps import AppConfig


class WardrobeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wardrobe"

    def ready(self):
        from . import signals  # noqa: F401
