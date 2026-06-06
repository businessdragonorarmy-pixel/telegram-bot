from __future__ import annotations

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def log_order_update(sender: type[Order], instance: Order, created: bool, **kwargs) -> None:
    if created:
        logger.info("New order created: %s", instance.reference_id)
    elif instance.status == Order.Status.PAID:
        logger.info("Order completed: %s", instance.reference_id)
