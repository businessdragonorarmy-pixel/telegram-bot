from __future__ import annotations

import logging

from django.conf import settings

import telegram
from telegram import Bot, Update
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramBotService:
    def __init__(self) -> None:
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.bot = Bot(token=self.token) if self.token else None

    def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: object | None = None,
        parse_mode: str = "Markdown",
    ) -> bool:
        if not self.bot:
            logger.warning("Telegram bot not configured")
            return False
        try:
            self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            return True
        except TelegramError as e:
            logger.exception("Failed to send message to %s: %s", chat_id, e)
            return False

    def send_photo(
        self,
        chat_id: int,
        photo: str | bytes,
        caption: str = "",
        reply_markup: object | None = None,
    ) -> bool:
        if not self.bot:
            return False
        try:
            self.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
            return True
        except TelegramError as e:
            logger.exception("Failed to send photo to %s: %s", chat_id, e)
            return False

    def send_document(
        self,
        chat_id: int,
        document: str | bytes,
        filename: str = "",
        caption: str = "",
    ) -> bool:
        if not self.bot:
            return False
        try:
            self.bot.send_document(
                chat_id=chat_id,
                document=document,
                filename=filename,
                caption=caption,
            )
            return True
        except TelegramError as e:
            logger.exception("Failed to send document to %s: %s", chat_id, e)
            return False

    def set_webhook(self, url: str) -> bool:
        if not self.bot:
            return False
        try:
            self.bot.set_webhook(url=url)
            logger.info("Webhook set to %s", url)
            return True
        except TelegramError as e:
            logger.exception("Failed to set webhook: %s", e)
            return False

    def delete_webhook(self) -> bool:
        if not self.bot:
            return False
        try:
            self.bot.delete_webhook()
            return True
        except TelegramError as e:
            logger.exception("Failed to delete webhook: %s", e)
            return False

    def broadcast_message(self, chat_ids: list[int], text: str) -> dict[str, list[int]]:
        result: dict[str, list[int]] = {"sent": [], "failed": []}
        for chat_id in chat_ids:
            success = self.send_message(chat_id, text)
            if success:
                result["sent"].append(chat_id)
            else:
                result["failed"].append(chat_id)
        return result
