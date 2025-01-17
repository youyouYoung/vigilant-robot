from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product, Order, Category, ProductImage
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, ProductImageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Category model.
    """
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # # Optionally, you can customize the queryset or add filtering here
    # def get_queryset(self):
    #     # For example, filter only active categories
    #     return Category.objects.filter(is_active=True)

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    商品图片View
    """
    permission_classes = [AllowAny]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
