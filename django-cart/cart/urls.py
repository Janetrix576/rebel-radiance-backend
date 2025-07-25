from django.urls import path
from .views import (
    ProductListAPIView,
    CartDetailAPIView,
    AddToCartAPIView,
    RemoveFromCartAPIView,
    UpdateCartItemAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('cart/update/<int:item_id>/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
]