import uuid

from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        EXPIRED = "EXPIRED", "Expired"

    user = models.ForeignKey(
        "accounts.TelegramUser", on_delete=models.CASCADE, related_name="orders", verbose_name="User"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="orders", verbose_name="Product"
    )
    plan = models.ForeignKey(
        "products.Plan", on_delete=models.CASCADE, related_name="orders", verbose_name="Plan"
    )
    reference_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, verbose_name="Reference ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(max_length=10, default="INR", verbose_name="Currency")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name="Status")
    payment_method = models.CharField(max_length=50, blank=True, default="", verbose_name="Payment Method")
    razorpay_order_id = models.CharField(max_length=100, blank=True, default="", verbose_name="Razorpay Order ID")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, default="", verbose_name="Razorpay Payment ID")
    key_assigned = models.CharField(max_length=500, blank=True, default="", verbose_name="Key Assigned")
    notes = models.TextField(blank=True, default="", verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.reference_id} - {self.user} - {self.product} - {self.status}"
