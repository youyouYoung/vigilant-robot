from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product, Category, ProductImage, ProductPriceHistory
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer, ProductPriceHistorySerializer
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import OrderingFilter


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Category model.
    """
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    # permission_classes = [AdminOnly]
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = ProductFilter
    ordering_fields = ['id', 'brand', 'category', 'is_featured', 'is_active', 'on_sale']  # 允许按这些字段排序
    ordering = ['id']  # 默认按 'price' 升序排序

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImage.objects.order_by('is_primary', '-id')
            )
        )

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    商品图片View
    """
    permission_classes = [AllowAny]
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk', None)
        return ProductImage.objects.filter(product_id=product_pk).order_by('-id')

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
