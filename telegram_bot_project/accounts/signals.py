from __future__ import annotations

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TelegramUser

logger = logging.getLogger(__name__)


@receiver(post_save, sender=TelegramUser)
def log_user_creation(sender: type[TelegramUser], instance: TelegramUser, created: bool, **kwargs) -> None:
    if created:
        logger.info("New Telegram user created: %s (%s)", instance.telegram_id, instance.username)
