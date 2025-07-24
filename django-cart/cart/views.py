from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from .serializers import (
    ProductSerializer,
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartAPIView(generics.GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': serializer.validated_data['quantity']}
        )

        if not created:
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()

        return Response(CartSerializer(cart, context=self.get_serializer_context()).data)

class RemoveFromCartAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)

class UpdateCartItemAPIView(generics.GenericAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()

    def put(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()

        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)