from rest_framework import viewsets, permissions
from .models import Product, Category, Tag
from .serializers import (
    ProductListSerializer, 
    ProductDetailSerializer, 
    CategorySerializer, 
    TagSerializer
)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        'category', 
        'tags', 
        'variants__attributes__attribute', 
        'images'
    )
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TagSerializer
