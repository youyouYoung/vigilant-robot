from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer