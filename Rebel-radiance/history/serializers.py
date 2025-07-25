from rest_framework import serializers
from .models import Product, Customer, OrderHistory, ProductChangeLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'

class ProductChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductChangeLog
        fields = '__all__'