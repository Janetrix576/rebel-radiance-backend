from django.shortcuts import render
from django.http import JsonResponse
from .models import OrderHistory

def customer_order_history(request, customer_id):
    orders = OrderHistory.objects.filter(customer_id=customer_id).order_by('-order_date')
    data = [{
        'product': order.product.name,
        'quantity': order.quantity,
        'date': order.order_date
    } for order in orders]
    return JsonResponse({'history': data})

