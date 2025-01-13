from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
