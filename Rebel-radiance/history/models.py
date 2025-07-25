from django.db import models
from django.conf import settings # <-- Import settings

# NOTE: We are now using settings.AUTH_USER_MODEL instead of the old User model

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # <-- FIXED
    phone = models.CharField(max_length=20)
    address = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)

class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)

class ProductChangeLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) # <-- FIXED
    change_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)