import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name')
    current_price_min = django_filters.NumberFilter(field_name='current_price', lookup_expr='gte')
    current_price_max = django_filters.NumberFilter(field_name='current_price', lookup_expr='lte')
    on_sale = django_filters.BooleanFilter(field_name='on_sale')

    class Meta:
        model = Product
        fields = ['brand', 'category','category_name','current_price_min','current_price_max','on_sale',]