from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    message = models.TextField(verbose_name="Message")
    image = models.ImageField(upload_to="announcements/", blank=True, null=True, verbose_name="Image")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Broadcast(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    title = models.CharField(max_length=255, verbose_name="Title")
    message = models.TextField(verbose_name="Message")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name="Status")
    total_count = models.PositiveIntegerField(default=0, verbose_name="Total Recipients")
    sent_count = models.PositiveIntegerField(default=0, verbose_name="Sent Count")
    failed_count = models.PositiveIntegerField(default=0, verbose_name="Failed Count")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="Completed At")

    class Meta:
        verbose_name = "Broadcast"
        verbose_name_plural = "Broadcasts"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class BroadcastLog(models.Model):
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE, related_name="logs", verbose_name="Broadcast")
    user = models.ForeignKey(
        "accounts.TelegramUser", on_delete=models.CASCADE, related_name="broadcast_logs", verbose_name="User"
    )
    status = models.CharField(max_length=20, default="PENDING", verbose_name="Status")
    error_message = models.TextField(blank=True, default="", verbose_name="Error Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Broadcast Log"
        verbose_name_plural = "Broadcast Logs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.broadcast.title} - {self.user}"
