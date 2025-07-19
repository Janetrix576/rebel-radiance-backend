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
    print("Old data has been cleared.")

def seed_data():
    print("Seeding new data...")

    print("Creating Tags...")
    tag_new, _ = Tag.objects.get_or_create(name="New Arrival")
    tag_unisex, _ = Tag.objects.get_or_create(name="Unisex")
    tag_men, _ = Tag.objects.get_or_create(name="For Men")
    tag_women, _ = Tag.objects.get_or_create(name="For Women")
    tag_bestseller, _ = Tag.objects.get_or_create(name="Bestseller")
    tag_eco, _ = Tag.objects.get_or_create(name="Eco-Friendly")

    print("Creating Attributes...")
    attr_size, _ = Attribute.objects.get_or_create(name="Size")
    val_s, _ = AttributeValue.objects.get_or_create(attribute=attr_size, value="S")
    val_m, _ = AttributeValue.objects.get_or_create(attribute=attr_size, value="M")
    val_l, _ = AttributeValue.objects.get_or_create(attribute=attr_size, value="L")

    attr_shoe_size, _ = Attribute.objects.get_or_create(name="Shoe Size (EU)")
    val_ss_38, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="38")
    val_ss_39, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="39")
    val_ss_41, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="41")
    val_ss_42, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="42")

    attr_volume, _ = Attribute.objects.get_or_create(name="Volume")
    val_v_50, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="50ml")
    val_v_100, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="100ml")
    val_v_250, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="250ml")

    print("Creating Categories...")
    cat_clothing, _ = Category.objects.get_or_create(name="Clothing", defaults={'slug': 'clothing'})
    cat_footwear, _ = Category.objects.get_or_create(name="Footwear", defaults={'slug': 'footwear'})
    cat_beauty, _ = Category.objects.get_or_create(name="Beauty Products", defaults={'slug': 'beauty'})
    cat_men_cloth, _ = Category.objects.get_or_create(name="Men's Clothing", defaults={'slug': 'men-clothing', 'parent': cat_clothing})
    cat_women_cloth, _ = Category.objects.get_or_create(name="Women's Clothing", defaults={'slug': 'women-clothing', 'parent': cat_clothing})
    cat_men_shoes, _ = Category.objects.get_or_create(name="Men's Shoes", defaults={'slug': 'men-shoes', 'parent': cat_footwear})
    cat_women_shoes, _ = Category.objects.get_or_create(name="Women's Shoes", defaults={'slug': 'women-shoes', 'parent': cat_footwear})
    cat_skincare, _ = Category.objects.get_or_create(name="Skincare", defaults={'slug': 'skincare', 'parent': cat_beauty})
    cat_haircare, _ = Category.objects.get_or_create(name="Haircare", defaults={'slug': 'haircare', 'parent': cat_beauty})

    product_definitions = [
        # == CLOTHING ==
        {'cat': cat_women_cloth, 'name': 'Thanh Hien 3-Piece Set', 'slug': 'thanh-hien-3-piece-set', 'desc': 'Easy to wear natural fashion set from Vietnam. Includes top, shorts, and over-shirt.', 'tags': [tag_women, tag_new], 'img': 'product_images/placeholder.jpg', 'variants': [(val_s, 817.12), (val_m, 817.12)]},
        {'cat': cat_women_cloth, 'name': 'Bohemian Floral Maxi Dress', 'slug': 'bohemian-maxi-dress', 'desc': 'A flowing, floral maxi dress perfect for summer days and casual evenings.', 'tags': [tag_women], 'img': 'product_images/placeholder.jpg', 'variants': [(val_s, 1250.00), (val_m, 1250.00), (val_l, 1250.00)]},
        {'cat': cat_women_cloth, 'name': 'High-Waisted Power Leggings', 'slug': 'power-leggings', 'desc': 'Comfortable and supportive high-waisted leggings for workouts or casual wear.', 'tags': [tag_women, tag_bestseller], 'img': 'product_images/placeholder.jpg', 'variants': [(val_s, 990.00), (val_m, 990.00)]},
        {'cat': cat_men_cloth, 'name': 'Classic Oxford Shirt', 'slug': 'classic-oxford-shirt', 'desc': 'A timeless and versatile Oxford shirt, essential for any man\'s wardrobe.', 'tags': [tag_men, tag_bestseller], 'img': 'product_images/placeholder.jpg', 'variants': [(val_m, 1100.00), (val_l, 1100.00)]},
        {'cat': cat_men_cloth, 'name': 'Performance Athletic Shorts', 'slug': 'performance-shorts', 'desc': 'Lightweight, breathable shorts designed for maximum performance.', 'tags': [tag_men], 'img': 'product_images/placeholder.jpg', 'variants': [(val_m, 850.00), (val_l, 850.00)]},
        {'cat': cat_clothing, 'name': 'Signature Unisex Hoodie', 'slug': 'signature-unisex-hoodie', 'desc': 'An iconic, premium-weight hoodie made from organic cotton. A staple for everyone.', 'tags': [tag_unisex, tag_eco], 'img': 'product_images/placeholder.jpg', 'variants': [(val_s, 1800.00), (val_m, 1800.00), (val_l, 1850.00)]},
        
        # == FOOTWEAR ==
        {'cat': cat_women_shoes, 'name': 'Autumn Casual Board Shoes', 'slug': 'autumn-board-shoes', 'desc': 'Unisex-style, breathable board shoes inspired by 2025 Wenzhou designs.', 'tags': [tag_women, tag_new], 'img': 'product_images/placeholder.jpg', 'variants': [(val_ss_38, 830.74), (val_ss_39, 830.74)]},
        {'cat': cat_men_shoes, 'name': 'Urban Explorer Sneakers', 'slug': 'urban-sneakers', 'desc': 'Versatile and comfortable unisex sneakers, sourced from Wenzhou King-Footwear.', 'tags': [tag_men, tag_bestseller], 'img': 'product_images/placeholder.jpg', 'variants': [(val_ss_41, 770.00), (val_ss_42, 770.00)]},
        {'cat': cat_women_shoes, 'name': 'Elegant Heeled Sandals', 'slug': 'heeled-sandals', 'desc': 'A pair of elegant sandals with a comfortable block heel, perfect for events.', 'tags': [tag_women], 'img': 'product_images/placeholder.jpg', 'variants': [(val_ss_38, 1400.00), (val_ss_39, 1400.00)]},
        {'cat': cat_men_shoes, 'name': 'Handcrafted Leather Boots', 'slug': 'leather-boots', 'desc': 'Durable, handcrafted leather boots that combine style and ruggedness.', 'tags': [tag_men], 'img': 'product_images/placeholder.jpg', 'variants': [(val_ss_41, 2800.00), (val_ss_42, 2800.00)]},
        {'cat': cat_women_shoes, 'name': 'Comfort Slip-On Flats', 'slug': 'slip-on-flats', 'desc': 'The perfect everyday shoe, combining style with all-day comfort.', 'tags': [tag_women], 'img': 'product_images/placeholder.jpg', 'variants': [(val_ss_38, 950.00), (val_ss_39, 950.00)]},
        {'cat': cat_men_shoes, 'name': 'Suede Driving Loafers', 'slug': 'driving-loafers', 'desc': 'Sophisticated suede loafers for a smart-casual look.', 'tags': [tag_men], 'img': 'product_images/placeholder.jpg', 'variants': [(val_ss_41, 2100.00), (val_ss_42, 2100.00)]},
        # == BEAUTY PRODUCTS ==
        {'cat': cat_skincare, 'name': 'Rejuvenating Vitamin C Serum', 'slug': 'vitamin-c-serum', 'desc': 'Brightens and revitalizes skin with a potent blend of antioxidants.', 'tags': [tag_unisex, tag_bestseller], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_50, 1200.00), (val_v_100, 2000.00)]},
        {'cat': cat_skincare, 'name': 'Hydrating Aloe Vera Gel', 'slug': 'aloe-vera-gel', 'desc': 'Soothes and hydrates skin with pure aloe vera extract.', 'tags': [tag_unisex], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_100, 800.00)]},
        {'cat': cat_skincare, 'name': 'Organic Green Tea Face Mask', 'slug': 'green-tea-mask', 'desc': 'Detoxifying face mask enriched with organic green tea.', 'tags': [tag_unisex, tag_eco], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_50, 950.00)]},
        {'cat': cat_skincare, 'name': 'Revitalizing Eye Cream', 'slug': 'eye-cream', 'desc': 'Reduces dark circles and puffiness for a refreshed look.', 'tags': [tag_unisex], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_250, 1500.00)]},
        {'cat': cat_haircare, 'name': 'Nourishing Argan Oil Shampoo', 'slug': 'argan-oil-shampoo', 'desc': 'Infused with argan oil to nourish and strengthen hair.', 'tags': [tag_unisex], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_250, 1100.00)]},
        {'cat': cat_haircare, 'name': 'Moisturizing Coconut Conditioner', 'slug': 'coconut-conditioner', 'desc': 'Deeply hydrates and detangles hair with coconut extract.', 'tags': [tag_unisex], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_250, 950.00)]},
        {'cat': cat_haircare, 'name': 'Revitalizing Hair Growth Serum', 'slug': 'hair-growth-serum', 'desc': 'Stimulates hair growth with a blend of natural oils.', 'tags': [tag_unisex, tag_bestseller], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_50, 1500.00)]},
        {'cat': cat_skincare, 'name': 'Synogal 7-Color LED Therapy Mask', 'slug': 'synogal-led-mask', 'desc': 'A home-use phototherapy mask for skin whitening and rejuvenation from Guangzhou.', 'tags': [tag_unisex, tag_new], 'img': 'product_images/placeholder.jpg', 'variants': [(None, 3268.45)]},
        {'cat': cat_skincare, 'name': 'Hydrating Hyaluronic Acid Serum', 'slug': 'hydrating-serum', 'desc': 'A powerful serum to lock in moisture for a youthful glow. For all skin types.', 'tags': [tag_unisex, tag_bestseller], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_50, 1100.00), (val_v_100, 1900.00)]},
        {'cat': cat_skincare, 'name': "Men's Revitalizing Face Wash", 'slug': 'men-face-wash', 'desc': 'A daily cleanser designed to remove grime and energize men\'s skin.', 'tags': [tag_men], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_100, 950.00)]},
        {'cat': cat_haircare, 'name': 'Argan Oil Repairing Hair Mask', 'slug': 'argan-hair-mask', 'desc': 'Deeply conditions and restores shine to dry or damaged hair.', 'tags': [tag_women], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_250, 1300.00)]},
        {'cat': cat_haircare, 'name': "Men's Firm Hold Styling Pomade", 'slug': 'men-pomade', 'desc': 'For a sharp, classic look with a strong hold and matte finish.', 'tags': [tag_men], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_100, 850.00)]},
        {'cat': cat_haircare, 'name': 'Tea Tree Scalp Treatment Shampoo', 'slug': 'tea-tree-shampoo', 'desc': 'A clarifying shampoo that soothes the scalp and removes buildup. For all.', 'tags': [tag_unisex, tag_eco], 'img': 'product_images/placeholder.jpg', 'variants': [(val_v_250, 1050.00)]},
    ]

    print("Creating Products and Variants...")
    for p_data in product_definitions:
        product, created = Product.objects.get_or_create(
            slug=p_data['slug'],
            defaults={
                'category': p_data['cat'],
                'name': p_data['name'],
                'description': p_data['desc'],
            }
        )
        if created:
            print(f"  - Created Product: {product.name}")
            product.tags.set(p_data['tags'])
            ProductImage.objects.create(product=product, image=p_data['img'], alt_text=f"Image of {product.name}")

            for attr_val, price in p_data['variants']:
                variant = ProductVariant.objects.create(product=product, price=price, stock_quantity=random.randint(5, 50))
                if attr_val:
                    variant.attributes.add(attr_val)
                print(f"    - Created Variant: {variant}")

    print("\nSeeding complete!")

if __name__ == '__main__':
    seed_data()