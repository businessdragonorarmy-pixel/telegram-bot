from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Banner, Category, Plan, Product
from .serializers import (
    BannerSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
    PlanSerializer,
    ProductKeyBulkCreateSerializer,
    ProductSerializer,
)
from .services import ProductKeyService


class BannerListAPIView(generics.ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.AllowAny]


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["category"]

    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related("plans")


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).prefetch_related("plans")
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class PlanListAPIView(generics.ListAPIView):
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["product", "is_active"]

    def get_queryset(self):
        return Plan.objects.filter(is_active=True).select_related("product")


class ProductKeyBulkCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductKeyBulkCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from .models import Product

        try:
            product = Product.objects.get(id=serializer.validated_data["product_id"])
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        keys = serializer.validated_data["keys"]
        created = ProductKeyService.bulk_create_keys(product, keys)

        return Response(
            {"message": f"Created {created} keys.", "total": len(keys), "created": created},
            status=status.HTTP_201_CREATED,
        )
