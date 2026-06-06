from __future__ import annotations

import logging

from django.utils import timezone

from accounts.services import TelegramUserService
from telegram_bot.services import TelegramBotService

from .models import Broadcast, BroadcastLog

logger = logging.getLogger(__name__)


def send_broadcast(broadcast_id: int) -> dict[str, int]:
    try:
        broadcast = Broadcast.objects.get(id=broadcast_id)
    except Broadcast.DoesNotExist:
        return {"error": "Broadcast not found"}

    broadcast.status = Broadcast.Status.SENDING
    broadcast.save(update_fields=["status"])

    users = TelegramUserService.get_all_users()
    broadcast.total_count = len(users)
    broadcast.save(update_fields=["total_count"])

    bot_service = TelegramBotService()
    sent = 0
    failed = 0

    for user in users:
        success = bot_service.send_message(
            chat_id=user.telegram_id,
            text=f"*\U0001f4e2 {broadcast.title}*\n\n{broadcast.message}",
        )

        BroadcastLog.objects.create(
            broadcast=broadcast,
            user=user,
            status="SENT" if success else "FAILED",
            error_message="" if success else "Failed to send",
        )

        if success:
            sent += 1
        else:
            failed += 1

    broadcast.status = Broadcast.Status.SENT
    broadcast.sent_count = sent
    broadcast.failed_count = failed
    broadcast.completed_at = timezone.now()
    broadcast.save(update_fields=["status", "sent_count", "failed_count", "completed_at"])

    logger.info("Broadcast %s completed: sent=%d, failed=%d", broadcast_id, sent, failed)
    return {"sent": sent, "failed": failed}
