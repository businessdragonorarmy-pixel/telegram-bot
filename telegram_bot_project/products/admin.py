import csv
import io
import logging

from django.contrib import admin, messages
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .models import Banner, Category, Plan, Product, ProductKey

logger = logging.getLogger(__name__)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["title", "description"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "is_active", "product_count", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    list_editable = ["position", "is_active"]
    prepopulated_fields = {"name": ("name",)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("products"))

    def product_count(self, obj):
        return obj.product_count

    product_count.short_description = "Products"


class PlanInlineAdmin(admin.TabularInline):
    model = Plan
    extra = 1
    fields = ["duration_days", "price_inr", "price_usd", "stock_enabled", "is_active"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "position", "is_active", "plan_count", "key_count", "created_at"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]
    list_editable = ["position", "is_active"]
    inlines = [PlanInlineAdmin]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            plan_count=Count("plans", distinct=True),
            key_count=Count("keys", distinct=True),
        )

    def plan_count(self, obj):
        return obj.plan_count

    plan_count.short_description = "Plans"

    def key_count(self, obj):
        return obj.key_count

    key_count.short_description = "Keys"


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["product", "duration_days", "price_inr", "stock_enabled", "is_active"]
    list_filter = ["is_active", "stock_enabled", "product__category"]
    search_fields = ["product__name"]


@admin.register(ProductKey)
class ProductKeyAdmin(admin.ModelAdmin):
    list_display = ["product", "key_value_short", "is_used", "used_by", "used_at", "created_at"]
    list_filter = ["is_used", "product", "product__category"]
    search_fields = ["key_value", "product__name"]
    readonly_fields = ["is_used", "used_by", "used_at"]
    actions = ["download_csv_template", "upload_csv"]

    def key_value_short(self, obj):
        return obj.key_value[:30] + ("..." if len(obj.key_value) > 30 else "")

    key_value_short.short_description = "Key"

    def download_csv_template(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="key_template.csv"'
        writer = csv.writer(response)
        writer.writerow(["key_value"])
        writer.writerow(["XXXX-XXXX-XXXX"])
        return response

    download_csv_template.short_description = "Download CSV Template"

    def upload_csv(self, request, queryset):
        if "csv_file" not in request.FILES:
            self.message_user(request, "Please select a CSV file to upload.", level="error")
            return HttpResponseRedirect(request.path)

        csv_file = request.FILES["csv_file"]
        product_id = request.POST.get("product")

        if not product_id:
            self.message_user(request, "Please select a product.", level="error")
            return HttpResponseRedirect(request.path)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            self.message_user(request, "Product not found.", level="error")
            return HttpResponseRedirect(request.path)

        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        created_count = 0
        error_count = 0

        for row in reader:
            key_value = row.get("key_value", "").strip()
            if not key_value:
                error_count += 1
                continue
            try:
                ProductKey.objects.create(product=product, key_value=key_value)
                created_count += 1
            except Exception as e:
                logger.error("Failed to create key %s: %s", key_value, e)
                error_count += 1

        self.message_user(
            request,
            f"Created {created_count} keys. Errors: {error_count}.",
            level="info",
        )
        return HttpResponseRedirect(request.path)

    upload_csv.short_description = "Upload CSV"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-csv/",
                self.admin_site.admin_view(self.upload_csv_view),
                name="products_productkey_upload_csv",
            ),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        if request.method == "POST":
            return self.upload_csv(request, None)
        products = Product.objects.filter(is_active=True)
        return render(request, "admin/productkey_upload_csv.html", {"products": products})
