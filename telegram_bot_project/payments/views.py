from __future__ import annotations

import json
import logging

from django.conf import settings
from django.http import HttpResponse

from rest_framework import permissions
from rest_framework.views import APIView

from .services import PaymentService

logger = logging.getLogger(__name__)


class RazorpayWebhookAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        if not webhook_secret:
            logger.warning("Razorpay webhook secret not configured")
            return HttpResponse(status=200)

        webhook_signature = request.META.get("HTTP_X_RAZORPAY_SIGNATURE", "")
        payload = request.body

        service = PaymentService()
        if not service.razorpay.verify_webhook_signature(payload, webhook_signature):
            logger.warning("Invalid webhook signature")
            return HttpResponse(status=400)

        event_data = json.loads(payload)
        event = event_data.get("event", "")

        logger.info("Razorpay webhook event: %s", event)
        service.handle_webhook_event(event, event_data.get("payload", {}))

        return HttpResponse(status=200)
