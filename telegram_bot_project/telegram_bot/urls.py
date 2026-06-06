from django.urls import path

from . import views

urlpatterns = [
    path("webhook/", views.webhook, name="telegram-webhook"),
    path("set-webhook/", views.set_webhook_view, name="telegram-set-webhook"),
]
