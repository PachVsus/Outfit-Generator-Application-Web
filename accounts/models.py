from django.db import models


class AccountDeletionFeedback(models.Model):
    reason = models.CharField(max_length=40)
    details = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "account deletion feedback"

    def __str__(self):
        return self.reason
