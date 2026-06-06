from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.services import TelegramUserService
from telegram_bot.services import TelegramBotService

from .models import Announcement, Broadcast
from .serializers import AnnouncementSerializer, BroadcastSerializer


class AnnouncementListAPIView(generics.ListAPIView):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.AllowAny]


class BroadcastCreateAPIView(generics.CreateAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        broadcast = serializer.save()
        from .tasks import send_broadcast
        send_broadcast(broadcast.id)
