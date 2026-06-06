from django.contrib import admin

from .models import Announcement, Broadcast, BroadcastLog


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["title", "message"]


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "total_count", "sent_count", "failed_count", "created_at"]
    list_filter = ["status"]
    search_fields = ["title"]
    actions = ["send_broadcast"]

    def send_broadcast(self, request, queryset):
        from .tasks import send_broadcast
        for broadcast in queryset:
            send_broadcast(broadcast.id)
        self.message_user(request, f"Sent {queryset.count()} broadcast(s).")

    send_broadcast.short_description = "Send selected broadcasts"


@admin.register(BroadcastLog)
class BroadcastLogAdmin(admin.ModelAdmin):
    list_display = ["broadcast", "user", "status", "created_at"]
    list_filter = ["status", "broadcast"]
    search_fields = ["user__username", "user__telegram_id"]
