from django.urls import path

from . import views

urlpatterns = [
    path("webhook/", views.RazorpayWebhookAPIView.as_view(), name="payment-webhook"),
]
