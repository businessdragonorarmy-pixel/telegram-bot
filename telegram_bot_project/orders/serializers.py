from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    plan_duration = serializers.CharField(source="plan.duration_days", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "reference_id",
            "product",
            "product_name",
            "plan",
            "plan_duration",
            "amount",
            "currency",
            "status",
            "payment_method",
            "key_assigned",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["reference_id", "status", "key_assigned", "created_at", "updated_at"]


class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    telegram_id = serializers.IntegerField()


class OrderListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    plan_duration = serializers.CharField(source="plan.duration_days", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "reference_id",
            "product_name",
            "plan_duration",
            "amount",
            "currency",
            "status",
            "created_at",
        ]
