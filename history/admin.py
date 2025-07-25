from django.contrib import admin
from .models import Customer, Product, OrderHistory, ProductChangeLog

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderHistory)
admin.site.register(ProductChangeLog)

