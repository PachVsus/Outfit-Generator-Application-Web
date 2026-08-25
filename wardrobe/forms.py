from pathlib import Path

from django import forms

from .constants import CLOTHING_TYPES, STYLES, WEATHERS
from .models import Garment

MAX_IMAGE_SIZE = 8 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = css


class GarmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Garment
        fields = ("image", "name", "clothing_type", "main_color", "secondary_color", "style", "weather")
        widgets = {"image": forms.ClearableFileInput(attrs={"accept": "image/jpeg,image/png,image/webp"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["secondary_color"].required = False
        self.apply_bootstrap()

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
        if getattr(image, "size", 0) > MAX_IMAGE_SIZE:
            raise forms.ValidationError("Images must be 8 MB or smaller.")
        content_type = getattr(image, "content_type", "")
        extension = Path(image.name).suffix.lower()
        if content_type and content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError("Use a JPG, PNG, or WebP image.")
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise forms.ValidationError("Use a JPG, PNG, or WebP image.")
        return image


class GeneratorForm(BootstrapFormMixin, forms.Form):
    style = forms.ChoiceField(choices=(("Any", "Any style"),) + tuple((style, style) for style in STYLES))
    weather = forms.ChoiceField(choices=tuple((weather, weather) for weather in WEATHERS))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class OutfitSaveForm(BootstrapFormMixin, forms.Form):
    name = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={"placeholder": "Optional outfit name"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
