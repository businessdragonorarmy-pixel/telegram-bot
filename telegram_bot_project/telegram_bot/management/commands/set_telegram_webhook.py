from __future__ import annotations

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from ...services import TelegramBotService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Set or delete the Telegram bot webhook"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            type=str,
            default="",
            help="Webhook URL (default: TELEGRAM_BOT_WEBHOOK_URL from settings)",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete the current webhook instead of setting it",
        )

    def handle(self, *args, **options):
        service = TelegramBotService()

        if options["delete"]:
            self.stdout.write("Deleting webhook...")
            if service.delete_webhook():
                self.stdout.write(self.style.SUCCESS("Webhook deleted successfully"))
            else:
                self.stdout.write(self.style.ERROR("Failed to delete webhook"))
            return

        url = options["url"] or settings.TELEGRAM_BOT_WEBHOOK_URL
        if not url:
            self.stdout.write(self.style.ERROR(
                "No webhook URL provided. Set TELEGRAM_BOT_WEBHOOK_URL in .env or pass --url."
            ))
            return

        self.stdout.write(f"Setting webhook to: {url}")
        if service.set_webhook(url):
            self.stdout.write(self.style.SUCCESS(f"Webhook set to {url}"))
            info = service.bot.get_webhook_info() if service.bot else None
            if info:
                self.stdout.write(f"Pending updates: {info.pending_update_count}")
        else:
            self.stdout.write(self.style.ERROR("Failed to set webhook. Check your token and URL."))
