from django.db import models


class SupportTicket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        CLOSED = "CLOSED", "Closed"

    user = models.ForeignKey(
        "accounts.TelegramUser", on_delete=models.CASCADE, related_name="support_tickets", verbose_name="User"
    )
    message = models.TextField(verbose_name="Message")
    admin_reply = models.TextField(blank=True, default="", verbose_name="Admin Reply")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Ticket #{self.id} - {self.user} - {self.status}"
