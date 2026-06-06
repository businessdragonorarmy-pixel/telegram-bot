from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ["telegram_id", "username", "first_name", "phone_number", "is_verified", "is_blocked", "created_at"]
    list_filter = ["is_verified", "is_blocked", "is_admin", "created_at"]
    search_fields = ["telegram_id", "username", "first_name", "last_name", "phone_number"]
    readonly_fields = ["telegram_id", "created_at", "updated_at"]
    list_editable = ["is_verified", "is_blocked"]
    fieldsets = [
        (
            "Telegram Info",
            {
                "fields": ["telegram_id", "username", "first_name", "last_name", "phone_number", "language_code"],
            },
        ),
        (
            "Status",
            {
                "fields": ["is_verified", "is_blocked", "is_admin"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]
