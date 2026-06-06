from __future__ import annotations

import logging

from django.db import transaction
from django.utils import timezone

from .models import Product, ProductKey

logger = logging.getLogger(__name__)


class ProductKeyService:
    @staticmethod
    def assign_key(product: Product, user) -> str | None:
        available_key = ProductKey.objects.filter(product=product, is_used=False).select_for_update(skip_locked=True).first()
        if not available_key:
            logger.warning("No available keys for product %s", product.name)
            return None

        available_key.is_used = True
        available_key.used_by = user
        available_key.used_at = timezone.now()
        available_key.save(update_fields=["is_used", "used_by", "used_at"])

        logger.info("Key %s assigned to user %s for product %s", available_key.key_value[:10], user.telegram_id, product.name)
        return available_key.key_value

    @staticmethod
    def get_available_key_count(product: Product) -> int:
        return ProductKey.objects.filter(product=product, is_used=False).count()

    @staticmethod
    def bulk_create_keys(product: Product, key_values: list[str]) -> int:
        created = 0
        for key_value in key_values:
            try:
                ProductKey.objects.create(product=product, key_value=key_value)
                created += 1
            except Exception as e:
                logger.error("Failed to create key %s: %s", key_value[:20], e)
        return created

    @staticmethod
    def get_total_keys_count() -> int:
        return ProductKey.objects.count()

    @staticmethod
    def get_used_keys_count() -> int:
        return ProductKey.objects.filter(is_used=True).count()

    @staticmethod
    def get_available_keys_count() -> int:
        return ProductKey.objects.filter(is_used=False).count()
