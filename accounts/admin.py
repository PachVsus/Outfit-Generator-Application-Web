from django.contrib import admin

from .models import AccountDeletionFeedback


@admin.register(AccountDeletionFeedback)
class AccountDeletionFeedbackAdmin(admin.ModelAdmin):
    list_display = ("reason", "details", "created_at")
    list_filter = ("reason", "created_at")
    readonly_fields = ("reason", "details", "created_at")
