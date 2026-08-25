import django.db.models.deletion
import wardrobe.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Garment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("clothing_type", models.CharField(choices=[("Shirt", "Shirt"), ("Jacket", "Jacket"), ("Pants", "Pants"), ("Underwear", "Underwear"), ("Shoes", "Shoes"), ("Watch", "Watch"), ("Cap", "Cap")], max_length=20)),
                ("main_color", models.CharField(choices=[(c, c) for c in ("Black", "White", "Gray", "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Brown", "Beige", "Navy", "Multicolor")], max_length=30)),
                ("secondary_color", models.CharField(blank=True, choices=[(c, c) for c in ("Black", "White", "Gray", "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Brown", "Beige", "Navy", "Multicolor")], max_length=30)),
                ("style", models.CharField(choices=[(s, s) for s in ("Casual", "Rock and Roll", "Glamrock", "Jock", "Streetwear", "Grunge", "Punk", "Classic", "Techwear", "Business Casual", "Minimalist", "Preppy", "Athleisure", "Goth", "K-pop Inspired", "Boho", "Formal", "Fantasy Casual")], max_length=40)),
                ("weather", models.CharField(choices=[(w, w) for w in ("Any", "Warm", "Cold", "Rainy")], default="Any", max_length=10)),
                ("image", models.ImageField(upload_to=wardrobe.models.garment_upload_path)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="garments", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="Outfit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=120)),
                ("style", models.CharField(default="Any", max_length=40)),
                ("weather", models.CharField(default="Any", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("garments", models.ManyToManyField(related_name="outfits", to="wardrobe.garment")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="outfits", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddIndex(model_name="garment", index=models.Index(fields=["owner", "clothing_type"], name="wardrobe_ga_owner_i_6c4fc1_idx")),
        migrations.AddIndex(model_name="garment", index=models.Index(fields=["owner", "style"], name="wardrobe_ga_owner_i_2133f3_idx")),
    ]
