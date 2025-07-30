from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Category, Product, ProductVariant, Attribute, AttributeValue, Tag
from decimal import Decimal

class ProductAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.volume_attr = Attribute.objects.create(name="Volume")
        cls.val_50ml = AttributeValue.objects.create(attribute=cls.volume_attr, value="50ml")
        cls.val_100ml = AttributeValue.objects.create(attribute=cls.volume_attr, value="100ml")

        cls.beauty_cat = Category.objects.create(name="Beauty", slug="beauty")
        cls.skincare_cat = Category.objects.create(name="Skincare", slug="skincare", parent=cls.beauty_cat)
        cls.fragrance_cat = Category.objects.create(name="Fragrance", slug="fragrance", parent=cls.beauty_cat)

        cls.bestseller_tag = Tag.objects.create(name="Bestseller")

        cls.serum = Product.objects.create(
            category=cls.skincare_cat,
            name="Rejuvenating Vitamin C Serum",
            slug="vitamin-c-serum",
            description="A test serum."
        )
        cls.serum.tags.add(cls.bestseller_tag)
        
        ProductVariant.objects.create(product=cls.serum, price=1200.00, stock_quantity=50)

        cls.perfume = Product.objects.create(
            category=cls.fragrance_cat,
            name="Noir Enigma Eau de Parfum",
            slug="noir-enigma-perfume",
            description="A test perfume."
        )
        perfume_50ml_variant = ProductVariant.objects.create(product=cls.perfume, price=4500.00, stock_quantity=30)
        perfume_50ml_variant.attributes.add(cls.val_50ml)
        
        perfume_100ml_variant = ProductVariant.objects.create(product=cls.perfume, price=6200.00, stock_quantity=20)
        perfume_100ml_variant.attributes.add(cls.val_100ml)

    def test_list_products_endpoint(self):
        url = reverse('product-list') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.perfume.name)

    def test_retrieve_single_product_details(self):
        url = reverse('product-detail', kwargs={'slug': self.perfume.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.perfume.name)
        self.assertEqual(len(response.data['variants']), 2)
        self.assertEqual(response.data['variants'][0]['attributes'][0]['value'], '50ml')

    def test_list_categories_endpoint(self):
        url = reverse('category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], self.beauty_cat.name)

    def test_product_list_data_format(self):
        url = reverse('product-list')
        response = self.client.get(url)
        
        product_data = response.data[0]
        
        self.assertIn('id', product_data)
        self.assertIn('name', product_data)
        self.assertIn('slug', product_data)
        self.assertIn('display_price', product_data)
        self.assertIn('main_image', product_data)
        self.assertIn('tags', product_data)
        
        self.assertNotIn('description', product_data)
        self.assertNotIn('variants', product_data)
        self.assertEqual(product_data['display_price'], Decimal('4500.00'))