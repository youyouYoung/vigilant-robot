from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter
from .views import OrderViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]