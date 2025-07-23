from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, help_text="A URL-friendly version of the category name.")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.URLField(max_length=1024, blank=True, null=True) 

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
    slug = models.SlugField(unique=True)
    description = models.TextField(help_text="A compelling description of the product.")
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
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        attribute_str = ", ".join([str(attr) for attr in self.attributes.all().order_by('attribute__name')])
        return f"{self.product.name} ({attribute_str})" if attribute_str else self.product.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.URLField(max_length=1024, help_text="Product image URL") # <-- CHANGED TO URLField
    alt_text = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"Image for {self.product.name}"
