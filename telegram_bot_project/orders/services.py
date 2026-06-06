from __future__ import annotations

import logging
import uuid

from django.utils import timezone

from .models import Order

logger = logging.getLogger(__name__)


class OrderService:
    @staticmethod
    def create_order(user, product, plan) -> Order:
        order = Order.objects.create(
            user=user,
            product=product,
            plan=plan,
            reference_id=str(uuid.uuid4()).replace("-", "").upper()[:16],
            amount=plan.price_inr,
            currency="INR",
            status=Order.Status.PENDING,
        )
        logger.info("Order created: %s for user %s", order.reference_id, user.telegram_id)
        return order

    @staticmethod
    def get_order_by_reference(reference_id: str) -> Order | None:
        try:
            return Order.objects.get(reference_id=reference_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_order_by_razorpay_order_id(razorpay_order_id: str) -> Order | None:
        try:
            return Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def mark_order_paid(order: Order, razorpay_payment_id: str = "", key_assigned: str = "") -> Order:
        order.status = Order.Status.PAID
        order.razorpay_payment_id = razorpay_payment_id
        if key_assigned:
            order.key_assigned = key_assigned
        order.save(update_fields=["status", "razorpay_payment_id", "key_assigned", "updated_at"])
        logger.info("Order %s marked as PAID", order.reference_id)
        return order

    @staticmethod
    def mark_order_failed(order: Order) -> Order:
        order.status = Order.Status.FAILED
        order.save(update_fields=["status", "updated_at"])
        logger.info("Order %s marked as FAILED", order.reference_id)
        return order

    @staticmethod
    def get_user_orders(user) -> list[Order]:
        return list(Order.objects.filter(user=user).select_related("product", "plan").order_by("-created_at"))

    @staticmethod
    def get_total_orders_count() -> int:
        return Order.objects.count()

    @staticmethod
    def get_today_orders_count() -> int:
        today = timezone.now().date()
        return Order.objects.filter(created_at__date=today).count()

    @staticmethod
    def get_total_revenue() -> float:
        from django.db.models import Sum
        result = Order.objects.filter(status=Order.Status.PAID).aggregate(total=Sum("amount"))
        return result["total"] or 0

    @staticmethod
    def get_today_revenue() -> float:
        from django.db.models import Sum
        today = timezone.now().date()
        result = Order.objects.filter(status=Order.Status.PAID, created_at__date=today).aggregate(total=Sum("amount"))
        return result["total"] or 0

    @staticmethod
    def get_pending_orders_count() -> int:
        return Order.objects.filter(status=Order.Status.PENDING).count()
