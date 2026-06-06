from django.contrib import admin

from .models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "message_short", "status", "created_at", "updated_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "user__telegram_id", "message"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["status"]
    fieldsets = [
        (
            "Ticket Info",
            {
                "fields": ["user", "message", "status"],
            },
        ),
        (
            "Reply",
            {
                "fields": ["admin_reply"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]

    def message_short(self, obj: SupportTicket) -> str:
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")

    message_short.short_description = "Message"
