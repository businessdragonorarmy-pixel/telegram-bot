from django.urls import path

from . import views

urlpatterns = [
    path("tickets/", views.SupportTicketListCreateAPIView.as_view(), name="ticket-list-create"),
    path("tickets/<int:pk>/", views.SupportTicketDetailAPIView.as_view(), name="ticket-detail"),
    path("tickets/<int:pk>/reply/", views.SupportTicketReplyAPIView.as_view(), name="ticket-reply"),
]
