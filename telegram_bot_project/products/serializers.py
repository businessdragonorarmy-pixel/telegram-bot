from rest_framework import serializers

from .models import Banner, Category, Plan, Product, ProductKey


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "duration_days", "price_inr", "price_usd", "stock_enabled", "is_active"]


class ProductSerializer(serializers.ModelSerializer):
    plans = PlanSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "image", "description", "category", "plans", "position", "is_active", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "image", "description", "category", "position", "is_active"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "description", "products", "position", "is_active"]


class CategoryListSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "image", "description", "product_count", "position", "is_active"]

    def get_product_count(self, obj) -> int:
        return obj.products.filter(is_active=True).count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "description", "products", "position", "is_active", "created_at"]


class ProductKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductKey
        fields = ["id", "product", "key_value", "is_used", "created_at"]
        read_only_fields = ["is_used", "created_at"]


class ProductKeyBulkCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    keys = serializers.ListField(child=serializers.CharField(max_length=500))

    def validate_keys(self, value: list[str]) -> list[str]:
        if not value:
            raise serializers.ValidationError("Keys list cannot be empty.")
        if len(value) > 1000:
            raise serializers.ValidationError("Maximum 1000 keys per batch.")
        return [k.strip() for k in value if k.strip()]
