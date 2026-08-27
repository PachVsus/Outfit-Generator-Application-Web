from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from wardrobe.models import Garment, GarmentStyle, Outfit


class OwnershipTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="test-password-123")
        self.other = User.objects.create_user("other", password="test-password-123")
        self.private_garment = Garment.objects.create(
            owner=self.other,
            name="Other user's jacket",
            clothing_type="Jacket",
            main_color="Black",
            weather="Cold",
            image="garments/private.jpg",
        )
        self.private_garment.styles.add(GarmentStyle.objects.get(name="Casual"))
        self.client.force_login(self.owner)

    def test_wardrobe_list_excludes_other_users_items(self):
        response = self.client.get(reverse("wardrobe:garment_list"))
        self.assertNotContains(response, self.private_garment.name)

    def test_cannot_edit_another_users_item(self):
        response = self.client.get(reverse("wardrobe:garment_update", args=[self.private_garment.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_another_users_item(self):
        response = self.client.post(reverse("wardrobe:garment_delete", args=[self.private_garment.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Garment.objects.filter(pk=self.private_garment.pk).exists())

    def test_cannot_view_another_users_saved_outfit(self):
        outfit = Outfit.objects.create(owner=self.other, name="Private outfit")
        outfit.garments.add(self.private_garment)
        response = self.client.get(reverse("wardrobe:outfit_detail", args=[outfit.pk]))
        self.assertEqual(response.status_code, 404)


class AuthenticationTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("wardrobe:dashboard"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('wardrobe:dashboard')}")

    def test_signup_logs_user_in(self):
        response = self.client.post(reverse("accounts:signup"), {
            "username": "new-user",
            "email": "new@example.com",
            "password1": "A-long-test-password-123!",
            "password2": "A-long-test-password-123!",
        })
        self.assertRedirects(response, reverse("wardrobe:dashboard"))
        self.assertIn("_auth_user_id", self.client.session)
