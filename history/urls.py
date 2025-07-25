from django.urls import path
from . import views

urlpatterns = [
    path('orders/<int:customer_id>/', views.customer_order_history, name='customer_order_history'),
]
