from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product, Order, Category, ProductImage, ProductPriceHistory
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, ProductImageSerializer, ProductPriceHistorySerializer

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
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk', None)
        return ProductImage.objects.filter(product_id=product_pk)

    def perform_create(self, serializer):
        product_pk = self.kwargs['product_pk']
        serializer.save(product_id=product_pk)

    def perform_update(self, serializer):
        product_pk = self.kwargs['product_pk']
        serializer.save(product_id=product_pk)

class ProductPriceHistoryView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductPriceHistorySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return ProductPriceHistory.objects.filter(product_id=product_id).order_by('-start_date')

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
