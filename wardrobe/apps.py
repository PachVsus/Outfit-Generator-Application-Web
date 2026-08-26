from django.apps import AppConfig


## Configuration class for the wardrobe app, specifying the default auto field type and the app name. It also imports signal handlers when the app is ready.
class WardrobeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wardrobe"

    def ready(self):
        from . import signals  # noqa: F401
