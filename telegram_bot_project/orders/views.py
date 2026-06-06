from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.models import TelegramUser
from accounts.services import TelegramUserService
from products.models import Plan, Product

from .models import Order
from .serializers import OrderCreateSerializer, OrderListSerializer, OrderSerializer
from .services import OrderService


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["status", "product", "currency"]

    def get_queryset(self):
        return Order.objects.all().select_related("user", "product", "plan").order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id = serializer.validated_data["telegram_id"]
        product_id = serializer.validated_data["product_id"]
        plan_id = serializer.validated_data["plan_id"]

        user = TelegramUserService.get_user(telegram_id)
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            plan = Plan.objects.get(id=plan_id, is_active=True, product=product)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)

        order = OrderService.create_order(user, product, plan)

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all().select_related("user", "product", "plan")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "reference_id"


class UserOrdersAPIView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        telegram_id = self.kwargs["telegram_id"]
        return Order.objects.filter(user__telegram_id=telegram_id).select_related("product", "plan").order_by("-created_at")
