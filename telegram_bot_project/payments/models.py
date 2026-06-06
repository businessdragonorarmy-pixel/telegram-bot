from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        CAPTURED = "CAPTURED", "Captured"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="payment", verbose_name="Order"
    )
    razorpay_order_id = models.CharField(max_length=100, blank=True, default="", verbose_name="Razorpay Order ID")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, default="", verbose_name="Razorpay Payment ID")
    razorpay_signature = models.CharField(max_length=500, blank=True, default="", verbose_name="Razorpay Signature")
    razorpay_qr_id = models.CharField(max_length=100, blank=True, default="", verbose_name="Razorpay QR ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(max_length=10, default="INR", verbose_name="Currency")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED, verbose_name="Status")
    gateway_response = models.JSONField(blank=True, default=dict, verbose_name="Gateway Response")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.razorpay_qr_id or self.razorpay_order_id} - {self.status}"
