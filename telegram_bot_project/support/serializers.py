from rest_framework import serializers

from .models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = SupportTicket
        fields = ["id", "user", "username", "message", "admin_reply", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "admin_reply", "status", "created_at", "updated_at"]


class SupportTicketCreateSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    message = serializers.CharField(max_length=2000)
