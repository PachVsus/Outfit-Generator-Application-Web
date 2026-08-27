from django.db import migrations, models


STYLE_NAMES = (
    "Casual", "Rock and Roll", "Glamrock", "Jock", "Streetwear", "Grunge",
    "Punk", "Classic", "Techwear", "Business Casual", "Minimalist", "Preppy",
    "Athleisure", "Goth", "K-pop Inspired", "Boho", "Formal", "Fantasy Casual",
)


def migrate_existing_styles(apps, schema_editor):
    Garment = apps.get_model("wardrobe", "Garment")
    GarmentStyle = apps.get_model("wardrobe", "GarmentStyle")
    styles = {name: GarmentStyle.objects.get_or_create(name=name)[0] for name in STYLE_NAMES}
    for garment in Garment.objects.exclude(style="").iterator():
        style = styles.get(garment.style)
        if style is None:
            style = GarmentStyle.objects.get_or_create(name=garment.style)[0]
        garment.styles.add(style)


def restore_primary_style(apps, schema_editor):
    Garment = apps.get_model("wardrobe", "Garment")
    for garment in Garment.objects.prefetch_related("styles").iterator():
        first_style = garment.styles.order_by("name").first()
        garment.style = first_style.name if first_style else "Casual"
        garment.save(update_fields=("style",))


class Migration(migrations.Migration):
    dependencies = [("wardrobe", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="GarmentStyle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=40, unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.AddField(
            model_name="garment",
            name="styles",
            field=models.ManyToManyField(related_name="garments", to="wardrobe.garmentstyle"),
        ),
        migrations.RunPython(migrate_existing_styles, restore_primary_style),
        migrations.RemoveIndex(model_name="garment", name="wardrobe_ga_owner_i_2133f3_idx"),
        migrations.RemoveField(model_name="garment", name="style"),
    ]
