import os
import django
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beautyshop.settings')
django.setup()

from products.models import Category, Tag, Attribute, AttributeValue, Product, ProductVariant

def clear_data():
    print("Deleting old data...")
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Attribute.objects.all().delete()
    Product.objects.all().delete()
    print("Old data cleared.")

def seed_data():
    print("Creating new data...")

    size_attr = Attribute.objects.create(name="Size")
    attr_s = AttributeValue.objects.create(attribute=size_attr, value="Small")
    attr_m = AttributeValue.objects.create(attribute=size_attr, value="Medium")
    attr_l = AttributeValue.objects.create(attribute=size_attr, value="Large")

    shoe_size_attr = Attribute.objects.create(name="Shoe Size")
    attr_41 = AttributeValue.objects.create(attribute=shoe_size_attr, value="41")
    attr_42 = AttributeValue.objects.create(attribute=shoe_size_attr, value="42")
    attr_43 = AttributeValue.objects.create(attribute=shoe_size_attr, value="43")

    clothing_cat = Category.objects.create(name="Clothing", slug="clothing")
    footwear_cat = Category.objects.create(name="Footwear", slug="footwear")

    new_arrival_tag = Tag.objects.create(name="New Arrival")
    unisex_tag = Tag.objects.create(name="Unisex")
    hoodie = Product.objects.create(
        category=clothing_cat,
        name="Mkurugenzi Classic Hoodie",
        slug="mkurugenzi-classic-hoodie",
        description="The iconic Mkurugenzi hoodie. Comfortable, stylish, and built to last. A unisex staple for any wardrobe."
    )
    hoodie.tags.add(unisex_tag, new_arrival_tag)

    # Hoodie
    hoodie_s = ProductVariant.objects.create(product=hoodie, price=2500.00, stock_quantity=20)
    hoodie_s.attributes.add(attr_s)
    hoodie_m = ProductVariant.objects.create(product=hoodie, price=2500.00, stock_quantity=30)
    hoodie_m.attributes.add(attr_m)
    hoodie_l = ProductVariant.objects.create(product=hoodie, price=2500.00, stock_quantity=15)
    hoodie_l.attributes.add(attr_l)
    print(f"Created Product: {hoodie.name}")

    sneakers = Product.objects.create(
        category=footwear_cat,
        name="Urban Explorer Sneakers",
        slug="urban-explorer-sneakers",
        description="Versatile and comfortable sneakers designed for the modern explorer. Perfect for any urban adventure."
    )
    sneakers.tags.add(unisex_tag)

    # Sneakers
    sneakers_41 = ProductVariant.objects.create(product=sneakers, price=3500.00, stock_quantity=25)
    sneakers_41.attributes.add(attr_41)
    sneakers_42 = ProductVariant.objects.create(product=sneakers, price=3500.00, stock_quantity=22)
    sneakers_42.attributes.add(attr_42)
    sneakers_43 = ProductVariant.objects.create(product=sneakers, price=3500.00, stock_quantity=18)
    sneakers_43.attributes.add(attr_43)
    print(f"Created Product: {sneakers.name}")

    print("\nSeeding complete!")

if __name__ == '__main__':
    clear_data()
    seed_data()
