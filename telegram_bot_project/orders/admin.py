from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "user",
        "product",
        "plan",
        "amount",
        "currency",
        "status",
        "payment_method",
        "created_at",
    ]
    list_filter = ["status", "currency", "created_at", "product"]
    search_fields = ["reference_id", "razorpay_order_id", "razorpay_payment_id", "user__telegram_id", "user__username"]
    readonly_fields = ["reference_id", "created_at", "updated_at"]
    list_editable = ["status"]
    fieldsets = [
        (
            "Order Info",
            {
                "fields": ["reference_id", "user", "product", "plan", "amount", "currency", "status"],
            },
        ),
        (
            "Payment",
            {
                "fields": ["payment_method", "razorpay_order_id", "razorpay_payment_id"],
            },
        ),
        (
            "Delivery",
            {
                "fields": ["key_assigned", "notes"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]
