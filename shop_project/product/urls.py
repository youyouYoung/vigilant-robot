from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ProductViewSet, CategoryViewSet, ProductImageViewSet, ProductPriceHistoryView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet, basename='products')

# 嵌套路由：/api/products/<int:product_id>/
products_router = NestedDefaultRouter(router, r'products', lookup='product')
products_router.register(r'images', ProductImageViewSet, basename='product-images')
products_router.register(r'price-history', ProductPriceHistoryView, basename='price-history')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
