# models.py
from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, help_text="A URL name.")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ('attribute', 'value') 
        ordering = ['value']

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text=" identifier for the product.")
    description = models.TextField(help_text="description of the product.")
    tags = models.ManyToManyField(Tag, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    attributes = models.ManyToManyField(AttributeValue)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Optional Stock Keeping Unit")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in KES")
    stock_quantity = models.PositiveIntegerField(default=10, help_text="Available stock for this variant.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        attribute_str = ", ".join([str(attr) for attr in self.attributes.all().order_by('attribute__name')])
        return f"{self.product.name} ({attribute_str})" if attribute_str else self.product.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.URLField(help_text="Product image URL")  # Using URLField instead of ImageField
    alt_text = models.CharField(max_length=255, blank=True, help_text="Alt text")

    def __str__(self):
        return f"Image for {self.product.name}"

# serializers.py
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

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'display_price', 'main_image', 'tags')

    def get_display_price(self, obj):
        cheapest_variant = obj.variants.filter(is_active=True).order_by('price').first()
        return cheapest_variant.price if cheapest_variant else None

    def get_main_image(self, obj):
        first_image = obj.images.first()
        return first_image.image if first_image else None

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'category', 'tags', 'variants', 'images')
