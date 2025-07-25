from django.urls import path
from .views import (
    CartDetailAPIView,
    AddToCartAPIView,
    RemoveFromCartAPIView,
    UpdateCartItemAPIView
)

urlpatterns = [
    path('', CartDetailAPIView.as_view(), name='cart-detail'),
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('remove/<int:item_id>/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('update/<int:item_id>/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
]