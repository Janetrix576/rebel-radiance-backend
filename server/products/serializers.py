from rest_framework import serializers
from .models import (
    Product, 
    Category, 
    Tag, 
    ProductImage, 
    ProductVariant, 
    AttributeValue
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'value']

class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)
    class Meta:
        model = ProductVariant
        fields = ['id', 'price', 'stock_quantity', 'attributes']

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'price', 'main_image']
    
    def get_main_image(self, obj):
        request = self.context.get('request')
        first_image = obj.images.first()
        if first_image:
            return request.build_absolute_uri(first_image.image.url)
        return None
    price = serializers.DecimalField(source='variants.first.price', max_digits=10, decimal_places=2, read_only=True)

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'tags', 'images', 'variants']