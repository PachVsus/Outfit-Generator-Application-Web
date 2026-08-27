from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import AccountDeletionFeedback


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="original",
            email="original@example.com",
            password="test-password-123",
        )
        self.client.force_login(self.user)

    def test_user_can_update_profile_details(self):
        response = self.client.post(reverse("accounts:profile"), {
            "username": "updated",
            "first_name": "Jamie",
            "last_name": "Style",
            "email": "updated@example.com",
        })
        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated")
        self.assertEqual(self.user.email, "updated@example.com")

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user("another", email="taken@example.com")
        response = self.client.post(reverse("accounts:profile"), {
            "username": "original",
            "email": "taken@example.com",
        })
        self.assertContains(response, "An account already uses this email address.")

    def test_user_can_change_password(self):
        response = self.client.post(reverse("accounts:password_change"), {
            "old_password": "test-password-123",
            "new_password1": "A-new-long-password-456!",
            "new_password2": "A-new-long-password-456!",
        })
        self.assertRedirects(response, reverse("accounts:password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("A-new-long-password-456!"))


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="recover-me",
            email="recovery@example.com",
            password="test-password-123",
        )

    def test_reset_email_contains_a_link_and_timeout_is_one_hour(self):
        response = self.client.post(reverse("accounts:password_reset"), {"email": self.user.email})
        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/accounts/password/reset/", mail.outbox[0].body)
        self.assertEqual(settings.PASSWORD_RESET_TIMEOUT, 3600)

    def test_unknown_email_does_not_reveal_account_status(self):
        response = self.client.post(reverse("accounts:password_reset"), {"email": "missing@example.com"})
        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(mail.outbox, [])


class AccountDeletionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("delete-me", password="test-password-123")
        self.client.force_login(self.user)

    def test_deletion_stores_anonymous_feedback(self):
        response = self.client.post(reverse("accounts:delete_account"), {
            "reason": "missing_features",
            "current_password": "test-password-123",
        })
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertTrue(AccountDeletionFeedback.objects.filter(reason="missing_features").exists())

    def test_skip_deletes_without_storing_feedback(self):
        response = self.client.post(reverse("accounts:delete_account"), {
            "skip": "1",
            "current_password": "test-password-123",
        })
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertEqual(AccountDeletionFeedback.objects.count(), 0)

    def test_wrong_password_prevents_deletion(self):
        response = self.client.post(reverse("accounts:delete_account"), {
            "skip": "1",
            "current_password": "wrong-password",
        })
        self.assertContains(response, "Your password is incorrect.")
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_other_reason_requires_details(self):
        response = self.client.post(reverse("accounts:delete_account"), {
            "reason": "other",
            "other_reason": "",
            "current_password": "test-password-123",
        })
        self.assertContains(response, "Please specify your reason.")
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
