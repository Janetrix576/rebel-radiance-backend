from rest_framework import viewsets, permissions
from .models import Product, Category, Tag
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    TagSerializer 
)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug' 

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None 