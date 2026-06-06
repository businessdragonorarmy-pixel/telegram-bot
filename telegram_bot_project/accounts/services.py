from __future__ import annotations

import logging

from .models import TelegramUser

logger = logging.getLogger(__name__)


class TelegramUserService:
    @staticmethod
    def get_or_create_user(
        telegram_id: int,
        username: str = "",
        first_name: str = "",
        last_name: str = "",
        language_code: str = "en",
    ) -> tuple[TelegramUser, bool]:
        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": username or "",
                "first_name": first_name or "",
                "last_name": last_name or "",
                "language_code": language_code or "en",
            },
        )
        if not created:
            changed = False
            if username and user.username != username:
                user.username = username
                changed = True
            if first_name and user.first_name != first_name:
                user.first_name = first_name
                changed = True
            if last_name and user.last_name != last_name:
                user.last_name = last_name
                changed = True
            if changed:
                user.save(update_fields=["username", "first_name", "last_name"])
        return user, created

    @staticmethod
    def verify_user(telegram_id: int, phone_number: str) -> TelegramUser | None:
        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
            user.phone_number = phone_number
            user.is_verified = True
            user.save(update_fields=["phone_number", "is_verified"])
            logger.info("User %s verified with phone %s", telegram_id, phone_number)
            return user
        except TelegramUser.DoesNotExist:
            logger.warning("User %s not found for verification", telegram_id)
            return None

    @staticmethod
    def get_user(telegram_id: int) -> TelegramUser | None:
        try:
            return TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            return None

    @staticmethod
    def get_all_users() -> list[TelegramUser]:
        return list(TelegramUser.objects.filter(is_blocked=False))

    @staticmethod
    def get_verified_users() -> list[TelegramUser]:
        return list(TelegramUser.objects.filter(is_verified=True, is_blocked=False))

    @staticmethod
    def get_user_count() -> int:
        return TelegramUser.objects.count()

    @staticmethod
    def get_today_user_count() -> int:
        from django.utils import timezone
        today = timezone.now().date()
        return TelegramUser.objects.filter(created_at__date=today).count()
