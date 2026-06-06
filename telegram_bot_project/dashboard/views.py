from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import TelegramUserService
from orders.services import OrderService
from products.services import ProductKeyService
from support.services import SupportService


class DashboardStatsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        stats = {
            "total_users": TelegramUserService.get_user_count(),
            "today_users": TelegramUserService.get_today_user_count(),
            "total_orders": OrderService.get_total_orders_count(),
            "today_orders": OrderService.get_today_orders_count(),
            "total_revenue": float(OrderService.get_total_revenue()),
            "today_revenue": float(OrderService.get_today_revenue()),
            "pending_orders": OrderService.get_pending_orders_count(),
            "available_keys": ProductKeyService.get_available_keys_count(),
            "used_keys": ProductKeyService.get_used_keys_count(),
            "open_tickets": SupportService.get_open_tickets_count(),
        }
        return Response(stats)
