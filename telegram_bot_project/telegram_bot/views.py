from __future__ import annotations

import json
import logging

from asgiref.sync import async_to_sync
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from telegram import Update
from telegram.ext import Application

from .handlers import get_handlers

logger = logging.getLogger(__name__)

_bot_app: Application | None = None


def get_bot_app() -> Application:
    global _bot_app
    if _bot_app is None:
        _bot_app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        for handler in get_handlers():
            _bot_app.add_handler(handler)
    return _bot_app


@csrf_exempt
@require_POST
def webhook(request) -> HttpResponse:
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    app = get_bot_app()
    update = Update.de_json(body, app.bot)

    if update:
        async_to_sync(app.process_update)(update)

    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def set_webhook_view(request) -> HttpResponse:
    from .services import TelegramBotService
    service = TelegramBotService()
    url = request.POST.get("url", settings.TELEGRAM_BOT_WEBHOOK_URL)
    if url:
        service.set_webhook(url)
        return HttpResponse(f"Webhook set to {url}")
    return HttpResponse("No URL provided", status=400)
