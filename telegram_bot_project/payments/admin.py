from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "razorpay_qr_id",
        "razorpay_payment_id",
        "amount",
        "currency",
        "status",
        "created_at",
    ]
    list_filter = ["status", "currency"]
    search_fields = ["razorpay_qr_id", "razorpay_payment_id", "order__reference_id"]
    readonly_fields = ["gateway_response", "created_at", "updated_at"]
