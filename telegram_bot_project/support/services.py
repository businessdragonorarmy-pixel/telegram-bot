from __future__ import annotations

import logging

from .models import SupportTicket

logger = logging.getLogger(__name__)


class SupportService:
    @staticmethod
    def create_ticket(user, message: str) -> SupportTicket:
        ticket = SupportTicket.objects.create(user=user, message=message)
        logger.info("Support ticket #%d created by user %s", ticket.id, user.telegram_id)
        return ticket

    @staticmethod
    def reply_to_ticket(ticket_id: int, reply: str) -> SupportTicket | None:
        try:
            ticket = SupportTicket.objects.get(id=ticket_id)
            ticket.admin_reply = reply
            ticket.status = SupportTicket.Status.CLOSED
            ticket.save(update_fields=["admin_reply", "status", "updated_at"])
            return ticket
        except SupportTicket.DoesNotExist:
            return None

    @staticmethod
    def get_user_tickets(user) -> list[SupportTicket]:
        return list(SupportTicket.objects.filter(user=user).order_by("-created_at"))

    @staticmethod
    def get_open_tickets_count() -> int:
        return SupportTicket.objects.filter(status=SupportTicket.Status.OPEN).count()
