from django.urls import path

from . import views

urlpatterns = [
    path("banners/", views.BannerListAPIView.as_view(), name="banner-list"),
    path("categories/", views.CategoryListAPIView.as_view(), name="category-list"),
    path("categories/<int:pk>/", views.CategoryDetailAPIView.as_view(), name="category-detail"),
    path("products/", views.ProductListAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductDetailAPIView.as_view(), name="product-detail"),
    path("plans/", views.PlanListAPIView.as_view(), name="plan-list"),
    path("keys/bulk-upload/", views.ProductKeyBulkCreateAPIView.as_view(), name="key-bulk-upload"),
]
