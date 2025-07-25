from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category
from .models import Cart, CartItem

User = get_user_model()

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(name="Test Cat", slug="test-cat")
        self.product1 = Product.objects.create(
            name='Test Product 1',
            slug='test-product-1',
            category=self.category
        )
        self.product1.variants.create(price=10.00)

        self.product2 = Product.objects.create(
            name='Test Product 2',
            slug='test-product-2',
            category=self.category
        )
        self.product2.variants.create(price=20.00)

    def test_add_to_cart(self):
        url = reverse('add-to-cart')
        data = {'product_id': self.product1.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)
        self.assertEqual(float(response.data['total_price']), 20.00)

    def test_get_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product1, quantity=3)
        
        url = reverse('cart-detail')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(float(response.data['total_price']), 30.00)

    def test_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product1, quantity=1)
        
        url = reverse('remove-from-cart', args=[item.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_update_cart_item(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product2, quantity=1)
        
        url = reverse('update-cart-item', args=[item.id])
        data = {'quantity': 5}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)
        self.assertEqual(float(response.data['total_price']), 100.00)