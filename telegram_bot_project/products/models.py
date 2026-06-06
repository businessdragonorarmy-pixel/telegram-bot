from django.db import models


class Banner(models.Model):
    image = models.ImageField(upload_to="banners/", verbose_name="Banner Image")
    title = models.CharField(max_length=255, blank=True, default="", verbose_name="Title")
    description = models.TextField(blank=True, default="", verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title or f"Banner #{self.id}"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category Name")
    image = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Category Image")
    description = models.TextField(blank=True, default="", verbose_name="Description")
    position = models.PositiveIntegerField(default=0, verbose_name="Position")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["position", "name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Product Image")
    description = models.TextField(blank=True, default="", verbose_name="Description")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="Category"
    )
    position = models.PositiveIntegerField(default=0, verbose_name="Position")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["position", "name"]

    def __str__(self) -> str:
        return self.name


class Plan(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="plans", verbose_name="Product"
    )
    duration_days = models.PositiveIntegerField(verbose_name="Duration (Days)")
    price_inr = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (INR)")
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Price (USD)")
    stock_enabled = models.BooleanField(default=True, verbose_name="Stock Enabled")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["product", "price_inr"]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.duration_days} Day(s) - ₹{self.price_inr}"


class ProductKey(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="keys", verbose_name="Product"
    )
    key_value = models.CharField(max_length=500, unique=True, verbose_name="Key")
    is_used = models.BooleanField(default=False, verbose_name="Is Used")
    used_by = models.ForeignKey(
        "accounts.TelegramUser",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="used_keys",
        verbose_name="Used By",
    )
    used_at = models.DateTimeField(blank=True, null=True, verbose_name="Used At")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Product Key"
        verbose_name_plural = "Product Keys"
        ordering = ["product", "-created_at"]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.key_value[:20]}..."
