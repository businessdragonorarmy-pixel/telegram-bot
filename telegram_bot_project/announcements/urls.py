from django.urls import path

from . import views

urlpatterns = [
    path("", views.AnnouncementListAPIView.as_view(), name="announcement-list"),
    path("broadcast/", views.BroadcastCreateAPIView.as_view(), name="broadcast-create"),
]
