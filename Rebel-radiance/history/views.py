# history/views.py
from rest_framework import viewsets
from .models import Product, Customer, OrderHistory, ProductChangeLog # Assuming these models exist
from .serializers import (
    ProductSerializer, CustomerSerializer, OrderHistorySerializer, ProductChangeLogSerializer
) # Assuming these serializers exist

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer

class ProductChangeLogViewSet(viewsets.ModelViewSet):
    queryset = ProductChangeLog.objects.all()
    serializer_class = ProductChangeLogSerializer