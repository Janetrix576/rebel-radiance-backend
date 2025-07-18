import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beautyshop.settings')
django.setup()

from products.models import Category, Tag, Attribute, AttributeValue, Product, ProductVariant, ProductImage

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
    
    volume_attr = Attribute.objects.create(name="Volume")
    attr_50ml = AttributeValue.objects.create(attribute=volume_attr, value="50ml")
    attr_100ml = AttributeValue.objects.create(attribute=volume_attr, value="100ml")

    clothing_cat = Category.objects.create(name="Clothing", slug="clothing")
    footwear_cat = Category.objects.create(name="Footwear", slug="footwear")
    perfume_cat = Category.objects.create(name="Perfumes", slug="perfumes")
    skincare_cat = Category.objects.create(name="Skin Care", slug="skin-care")
    haircare_cat = Category.objects.create(name="Hair Products", slug="hair-products")

    new_arrival_tag = Tag.objects.create(name="New Arrival")
    unisex_tag = Tag.objects.create(name="Unisex")
    mens_tag = Tag.objects.create(name="For Men")
    womens_tag = Tag.objects.create(name="For Women")

    hoodie = Product.objects.create(category=clothing_cat, name="Mkurugenzi Classic Hoodie", slug="mkurugenzi-classic-hoodie", description="The iconic Mkurugenzi hoodie. A unisex staple.")
    hoodie.tags.add(unisex_tag, new_arrival_tag)
    ProductImage.objects.create(product=hoodie, image='product_images/hoodie_front.jpg', alt_text="Front view of the Mkurugenzi Hoodie")
    ProductImage.objects.create(product=hoodie, image='product_images/hoodie_detail.jpg', alt_text="Detail shot of the Mkurugenzi Hoodie fabric")
    
    hoodie_s = ProductVariant.objects.create(product=hoodie, price=2500.00, stock_quantity=20)
    hoodie_s.attributes.add(attr_s)
    hoodie_m = ProductVariant.objects.create(product=hoodie, price=2500.00, stock_quantity=30)
    hoodie_m.attributes.add(attr_m)
    hoodie_l = ProductVariant.objects.create(product=hoodie, price=2500.00, stock_quantity=15)
    hoodie_l.attributes.add(attr_l)
    print(f"Created Product: {hoodie.name}")

    sneakers = Product.objects.create(category=footwear_cat, name="Urban Explorer Sneakers", slug="urban-explorer-sneakers", description="Versatile and comfortable unisex sneakers.")
    sneakers.tags.add(unisex_tag)
    ProductImage.objects.create(product=sneakers, image='product_images/sneakers_side.jpg', alt_text="Side view of the Urban Explorer Sneakers")
    ProductImage.objects.create(product=sneakers, image='product_images/sneakers_top.jpg', alt_text="Top-down view of the Urban Explorer Sneakers")

    sneakers_41 = ProductVariant.objects.create(product=sneakers, price=3500.00, stock_quantity=25)
    sneakers_41.attributes.add(attr_41)
    sneakers_42 = ProductVariant.objects.create(product=sneakers, price=3500.00, stock_quantity=22)
    sneakers_42.attributes.add(attr_42)
    sneakers_43 = ProductVariant.objects.create(product=sneakers, price=3500.00, stock_quantity=18)
    sneakers_43.attributes.add(attr_43)
    print(f"Created Product: {sneakers.name}")

    mens_perfume = Product.objects.create(category=perfume_cat, name="Noir Enigma", slug="noir-enigma-perfume", description="A bold and mysterious scent for the modern man. Notes of spice and wood.")
    mens_perfume.tags.add(mens_tag, new_arrival_tag)
    ProductImage.objects.create(product=mens_perfume, image='product_images/mens_perfume_bottle.jpg', alt_text="Noir Enigma perfume bottle")
    ProductImage.objects.create(product=mens_perfume, image='product_images/mens_perfume_box.jpg', alt_text="Noir Enigma perfume packaging")
    perfume_50 = ProductVariant.objects.create(product=mens_perfume, price=4500.00, stock_quantity=40)
    perfume_50.attributes.add(attr_50ml)
    perfume_100 = ProductVariant.objects.create(product=mens_perfume, price=6200.00, stock_quantity=25)
    perfume_100.attributes.add(attr_100ml)
    print(f"Created Product: {mens_perfume.name}")

    womens_perfume = Product.objects.create(category=perfume_cat, name="Velvet Bloom", slug="velvet-bloom-perfume", description="An elegant and floral fragrance for women. Delicate notes of jasmine and rose.")
    womens_perfume.tags.add(womens_tag)
    ProductImage.objects.create(product=womens_perfume, image='product_images/womens_perfume_bottle.jpg', alt_text="Velvet Bloom perfume bottle")
    w_perfume_50 = ProductVariant.objects.create(product=womens_perfume, price=4800.00, stock_quantity=50)
    w_perfume_50.attributes.add(attr_50ml)
    w_perfume_100 = ProductVariant.objects.create(product=womens_perfume, price=6500.00, stock_quantity=30)
    w_perfume_100.attributes.add(attr_100ml)
    print(f"Created Product: {womens_perfume.name}")

    face_serum = Product.objects.create(category=skincare_cat, name="Revitalizing Face Serum", slug="revitalizing-face-serum", description="A hydrating and brightening serum for all skin types. Packed with Vitamin C.")
    face_serum.tags.add(unisex_tag)
    ProductImage.objects.create(product=face_serum, image='product_images/serum_bottle.jpg', alt_text="Revitalizing Face Serum bottle")
    ProductImage.objects.create(product=face_serum, image='product_images/serum_texture.jpg', alt_text="Texture of the Revitalizing Face Serum")
    ProductVariant.objects.create(product=face_serum, price=2800.00, stock_quantity=60)
    print(f"Created Product: {face_serum.name}")

    hair_oil = Product.objects.create(category=haircare_cat, name="Nourishing Hair Oil", slug="nourishing-hair-oil", description="A blend of natural oils to strengthen and add shine to your hair.")
    hair_oil.tags.add(unisex_tag)
    ProductImage.objects.create(product=hair_oil, image='product_images/hair_oil_bottle.jpg', alt_text="Nourishing Hair Oil bottle")
    ProductVariant.objects.create(product=hair_oil, price=1800.00, stock_quantity=75)
    print(f"Created Product: {hair_oil.name}")

    print("\nSeeding complete!")

if __name__ == '__main__':
    clear_data()
    seed_data()