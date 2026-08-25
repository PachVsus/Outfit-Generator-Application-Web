import random

from django.contrib.auth.models import User
from django.test import TestCase

from wardrobe.models import Garment
from wardrobe.services import generate_outfit


class GeneratorServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("stylist", password="test-password-123")

    def garment(self, **overrides):
        values = {
            "owner": self.user,
            "name": "Test garment",
            "clothing_type": "Shirt",
            "main_color": "Black",
            "style": "Casual",
            "weather": "Any",
            "image": "garments/test.jpg",
        }
        values.update(overrides)
        return Garment.objects.create(**values)

    def test_returns_one_matching_item_per_category(self):
        shirt = self.garment(name="Warm shirt", weather="Warm")
        shoes = self.garment(name="Shoes", clothing_type="Shoes")
        self.garment(name="Cold goth shirt", style="Goth", weather="Cold")

        result = generate_outfit(self.user.garments.all(), "Casual", "Warm", random.Random(3))

        self.assertEqual({item.pk for item in result}, {shirt.pk, shoes.pk})
        self.assertEqual(len({item.clothing_type for item in result}), len(result))

    def test_never_selects_another_users_garments_when_given_owned_queryset(self):
        stranger = User.objects.create_user("stranger")
        Garment.objects.create(owner=stranger, name="Private shirt", clothing_type="Shirt", main_color="Red", style="Casual", weather="Any", image="garments/private.jpg")

        result = generate_outfit(self.user.garments.all())

        self.assertEqual(result, [])
