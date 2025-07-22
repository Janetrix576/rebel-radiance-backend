from rest_framework import serializers
from .models import Category, Tag, Attribute, AttributeValue, Product, ProductVariant, ProductImage

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'alt_text')

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()

    class Meta:
        model = AttributeValue
        fields = ('attribute', 'value')

class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'price', 'stock_quantity', 'attributes')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = TagSerializer(many=True, read_only=True)
    display_price = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    description = serializers.CharField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'description', 'display_price', 'main_image', 'tags')

    def get_display_price(self, obj):
        cheapest_variant = obj.variants.filter(is_active=True).order_by('price').first()
        return cheapest_variant.price if cheapest_variant else None

    def get_main_image(self, obj):
        image_obj = obj.images.first()
        if image_obj and image_obj.image:
            request = self.context.get('request')
            image_url = image_obj.image.url if hasattr(image_obj.image, 'url') else str(image_obj.image)
            return request.build_absolute_uri(image_url) if request else image_url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'category', 'tags', 'variants', 'images')
