from rest_framework import generics, permissions

from .models import TelegramUser
from .serializers import TelegramUserDetailSerializer, TelegramUserSerializer


class TelegramUserListAPIView(generics.ListAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["telegram_id", "username", "first_name", "phone_number"]


class TelegramUserDetailAPIView(generics.RetrieveAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "telegram_id"
