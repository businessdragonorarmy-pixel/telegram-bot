from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, blank=True, default="", verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, default="", verbose_name="First Name")
    last_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Last Name")
    phone_number = models.CharField(max_length=20, blank=True, default="", verbose_name="Phone Number")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    language_code = models.CharField(max_length=10, blank=True, default="en", verbose_name="Language Code")
    is_blocked = models.BooleanField(default=False, verbose_name="Is Blocked")
    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.username or self.first_name or str(self.telegram_id)
