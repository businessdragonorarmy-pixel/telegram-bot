from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.TelegramUserListAPIView.as_view(), name="user-list"),
    path("users/<int:telegram_id>/", views.TelegramUserDetailAPIView.as_view(), name="user-detail"),
]
