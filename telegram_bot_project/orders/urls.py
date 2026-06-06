from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrderListCreateAPIView.as_view(), name="order-list-create"),
    path("<str:reference_id>/", views.OrderDetailAPIView.as_view(), name="order-detail"),
    path("user/<int:telegram_id>/", views.UserOrdersAPIView.as_view(), name="user-orders"),
]
