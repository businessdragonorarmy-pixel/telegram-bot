from rest_framework import serializers

from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = [
            "id",
            "telegram_id",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "is_verified",
            "language_code",
            "created_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at"]


class TelegramUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = "__all__"
        read_only_fields = ["telegram_id", "created_at", "updated_at"]
