from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.services import TelegramUserService

from .models import SupportTicket
from .serializers import SupportTicketCreateSerializer, SupportTicketSerializer
from .services import SupportService


class SupportTicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all().select_related("user").order_by("-created_at")
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["status"]

    def create(self, request, *args, **kwargs):
        serializer = SupportTicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = TelegramUserService.get_user(serializer.validated_data["telegram_id"])
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        ticket = SupportService.create_ticket(user, serializer.validated_data["message"])

        return Response(
            SupportTicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED,
        )


class SupportTicketDetailAPIView(generics.RetrieveAPIView):
    queryset = SupportTicket.objects.all().select_related("user")
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAdminUser]


class SupportTicketReplyAPIView(generics.UpdateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        admin_reply = request.data.get("admin_reply", "")

        if not admin_reply:
            return Response({"error": "Reply is required."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = SupportService.reply_to_ticket(ticket.id, admin_reply)
        if not ticket:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(SupportTicketSerializer(ticket).data)
