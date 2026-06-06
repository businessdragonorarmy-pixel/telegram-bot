from __future__ import annotations

import hashlib
import hmac
import io
import logging

import requests
from django.conf import settings

import razorpay

from .models import Payment

logger = logging.getLogger(__name__)


class RazorpayClient:
    def __init__(self) -> None:
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def create_order(self, amount: float, currency: str = "INR", reference_id: str = "") -> dict:
        order_data = {
            "amount": int(amount * 100),
            "currency": currency,
            "receipt": reference_id,
            "payment_capture": 1,
        }
        order = self.client.order.create(order_data)
        logger.info("Razorpay order created: %s", order["id"])
        return order

    def create_qr_code(self, amount: float, reference_id: str, currency: str = "INR") -> dict:
        qr_data = {
            "type": "upi_qr",
            "name": "Store Payment",
            "usage": "single_use",
            "fixed_amount": True,
            "payment_amount": int(amount * 100),
            "description": f"Order {reference_id}",
            "notes": {"reference_id": reference_id},
        }
        qr = self.client.qr_code.create(qr_data)
        logger.info("Razorpay QR created: %s for order %s", qr["id"], reference_id)
        return qr

    def fetch_qr_code(self, qr_id: str) -> dict:
        return self.client.qr_code.fetch(qr_id)

    def download_qr_image(self, image_url: str) -> io.BytesIO:
        resp = requests.get(image_url, timeout=10)
        resp.raise_for_status()
        return io.BytesIO(resp.content)

    def verify_payment(self, razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
        params = f"{razorpay_order_id}|{razorpay_payment_id}"
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            params.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected_signature, razorpay_signature)

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)


class PaymentService:
    def __init__(self) -> None:
        self.razorpay = RazorpayClient()

    def create_qr_payment(self, order) -> tuple[Payment, dict, io.BytesIO]:
        razorpay_qr = self.razorpay.create_qr_code(
            amount=float(order.amount),
            reference_id=order.reference_id,
            currency=order.currency,
        )

        payment = Payment.objects.create(
            order=order,
            razorpay_qr_id=razorpay_qr["id"],
            amount=order.amount,
            currency=order.currency,
            status=Payment.Status.CREATED,
        )

        qr_image = self.razorpay.download_qr_image(razorpay_qr["image_url"])

        return payment, razorpay_qr, qr_image

    def handle_webhook_event(self, event: str, payload: dict) -> bool:
        if event == "payment.captured":
            return self._handle_payment_captured(payload)
        elif event == "payment.failed":
            return self._handle_payment_failed(payload)
        return False

    def _resolve_order_from_payload(self, payment_entity: dict):
        qr_id = payment_entity.get("qr_id", "")
        if qr_id:
            try:
                qr_data = self.razorpay.fetch_qr_code(qr_id)
                notes = qr_data.get("notes", {})
                reference_id = notes.get("reference_id", "")
                if reference_id:
                    from orders.models import Order
                    try:
                        return Order.objects.get(reference_id=reference_id)
                    except Order.DoesNotExist:
                        pass
            except Exception as e:
                logger.warning("Failed to resolve order via QR %s: %s", qr_id, e)

        razorpay_order_id = payment_entity.get("order_id", "")
        if razorpay_order_id:
            from orders.models import Order
            try:
                return Order.objects.get(razorpay_order_id=razorpay_order_id)
            except Order.DoesNotExist:
                pass

        return None

    def _handle_payment_captured(self, payload: dict) -> bool:
        payment_data = payload.get("payment", {}).get("entity", {})
        razorpay_payment_id = payment_data.get("id", "")

        order = self._resolve_order_from_payload(payment_data)
        if not order:
            logger.error("Could not resolve order from payment payload")
            return False

        from orders.services import OrderService
        from products.services import ProductKeyService

        key = ProductKeyService.assign_key(order.product, order.user)
        OrderService.mark_order_paid(order, razorpay_payment_id=razorpay_payment_id, key_assigned=key or "")

        try:
            payment = Payment.objects.get(order=order)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.status = Payment.Status.CAPTURED
            payment.gateway_response = payment_data
            payment.save(update_fields=["razorpay_payment_id", "status", "gateway_response", "updated_at"])
        except Payment.DoesNotExist:
            logger.warning("Payment record not found for order %s", order.reference_id)

        logger.info("Payment captured for order %s, key: %s", order.reference_id, key)
        return True

    def _handle_payment_failed(self, payload: dict) -> bool:
        payment_data = payload.get("payment", {}).get("entity", {})

        order = self._resolve_order_from_payload(payment_data)
        if not order:
            return False

        from orders.services import OrderService
        OrderService.mark_order_failed(order)

        try:
            payment = Payment.objects.get(order=order)
            payment.status = Payment.Status.FAILED
            payment.gateway_response = payment_data
            payment.save(update_fields=["status", "gateway_response", "updated_at"])
        except Payment.DoesNotExist:
            pass

        return True
