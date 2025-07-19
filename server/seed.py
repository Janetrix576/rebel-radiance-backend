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
    val_ss_36, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="36")
    val_ss_37, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="37")
    val_ss_38, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="38")
    val_ss_39, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="39")
    val_ss_41, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="41")
    val_ss_42, _ = AttributeValue.objects.get_or_create(attribute=attr_shoe_size, value="42")

    attr_volume, _ = Attribute.objects.get_or_create(name="Volume")
    val_v_50, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="50ml")
    val_v_100, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="100ml")
    val_v_250, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="250ml")
    val_v_500, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="500ml")
    val_v_1000, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="1000ml")

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
    
    # CLOTHING
    product_definitions = [
        {'cat': cat_women_cloth, 'name': 'Thanh Hien 3-Piece Set', 'slug': 'thanh-hien-3-piece-set', 'desc': 'Easy to wear natural fashion set from Vietnam. Includes top, shorts, and over-shirt.', 'tags': [tag_women, tag_new], 'img': 'https://i.pinimg.com/1200x/bc/62/ec/bc62ec18c79b3fb961457fe9b4258f1e.jpg', 'variants': [(val_s, 817.12), (val_m, 817.12)]},
        {'cat': cat_women_cloth, 'name': 'Bohemian Floral Maxi Dress', 'slug': 'bohemian-maxi-dress', 'desc': 'A flowing, floral maxi dress perfect for summer days and casual evenings.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/bd/cd/cf/bdcdcf6c22fa40a4fb836fc6154f81cf.jpg', 'variants': [(val_s, 1250.00), (val_m, 1250.00), (val_l, 1250.00)]},
        {'cat': cat_women_cloth, 'name': 'High-Waisted Power Leggings', 'slug': 'power-leggings', 'desc': 'Comfortable and supportive high-waisted leggings for workouts or casual wear.', 'tags': [tag_women, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/fd/47/8a/fd478a9b6b4aee135be44666b93c21b9.jpg', 'variants': [(val_s, 990.00), (val_m, 990.00)]},
        {'cat': cat_women_cloth, 'name': 'Elegant Silk Blouse', 'slug': 'elegant-silk-blouse', 'desc': 'A luxurious and versatile silk blouse that transitions effortlessly from office to evening wear.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/36/01/d7/3601d70cc150a8a28fb75868bac7c79d.jpg', 'variants': [(val_s, 1500.00), (val_m, 1500.00), (val_l, 1500.00)]},
        {'cat': cat_women_cloth, 'name': 'Chic Tailored Blazer', 'slug': 'chic-tailored-blazer', 'desc': 'A sharply tailored blazer that adds a touch of sophistication to any outfit.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/11/5b/c4/115bc4ffaeed39a16f1cdfac4a2324ac.jpg', 'variants': [(val_s, 2200.00), (val_m, 2200.00)]},
        {'cat': cat_men_cloth, 'name': 'Classic Oxford Shirt', 'slug': 'classic-oxford-shirt', 'desc': 'A timeless and versatile Oxford shirt, essential for any man\'s wardrobe. Made with 100% cotton.', 'tags': [tag_men, tag_bestseller], 'img': 'https://i.pinimg.com/736x/d1/9e/89/d19e89cfe9adfd2e0796f95501bb2737.jpg', 'variants': [(val_m, 1100.00), (val_l, 1100.00)]},
        {'cat': cat_men_cloth, 'name': 'Performance Athletic Shorts', 'slug': 'performance-shorts', 'desc': 'Lightweight, breathable shorts with sweat-wicking technology, designed for maximum performance.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/6e/bf/3b/6ebf3b69dfd7be4cf1b5dbbfca22fa4b.jpg', 'variants': [(val_m, 850.00), (val_l, 850.00)]},
        {'cat': cat_men_cloth, 'name': 'Modern Slim-Fit Chinos', 'slug': 'modern-slim-fit-chinos', 'desc': 'Versatile slim-fit chinos crafted with a hint of stretch for all-day comfort and style.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/d3/a6/ba/d3a6ba0740c7e03ee3e6731be39f74b3.jpg', 'variants': [(val_m, 1400.00), (val_l, 1400.00)]},
        {'cat': cat_men_cloth, 'name': 'Essential Pique Polo Shirt', 'slug': 'essential-pique-polo', 'desc': 'A classic pique polo shirt that offers a smart-casual look for any occasion.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/736x/5b/ef/c0/5befc07df0c685f7b5c1b67bec96ffa1.jpg', 'variants': [(val_s, 950.00), (val_m, 950.00), (val_l, 950.00)]},
        {'cat': cat_men_cloth, 'name': 'Lightweight Bomber Jacket', 'slug': 'lightweight-bomber-jacket', 'desc': 'A stylish and lightweight bomber jacket, perfect for layering during transitional weather.', 'tags': [tag_men, tag_new], 'img': 'https://i.pinimg.com/736x/ef/fc/d3/effcd3359a2e04f3a8f3d48b11d5fdda.jpg', 'variants': [(val_m, 2500.00), (val_l, 2500.00)]},
        {'cat': cat_clothing, 'name': 'Signature Unisex Hoodie', 'slug': 'signature-unisex-hoodie', 'desc': 'An iconic, premium-weight hoodie made from organic cotton. A staple for everyone.', 'tags': [tag_unisex, tag_eco, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/22/c6/fb/22c6fb0eccc73ea7ed246b345042c33d.jpg', 'variants': [(val_s, 1800.00), (val_m, 1800.00), (val_l, 1850.00)]},
        {'cat': cat_clothing, 'name': 'Classic Crewneck T-Shirt', 'slug': 'classic-crewneck-tshirt', 'desc': 'The perfect everyday essential. A soft, durable crewneck t-shirt available in multiple colors.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/0f/1b/f8/0f1bf87820aa11601d18875ecbf244ef.jpg', 'variants': [(val_s, 750.00), (val_m, 750.00), (val_l, 750.00)]},
        {'cat': cat_clothing, 'name': 'Vintage Denim Jacket', 'slug': 'vintage-denim-jacket', 'desc': 'A timeless denim jacket with a classic vintage wash that gets better with every wear.', 'tags': [tag_unisex, tag_new], 'img': 'https://i.pinimg.com/736x/5e/36/09/5e3609e33ecf087c130aeda6a55640c7.jpg', 'variants': [(val_s, 2800.00), (val_m, 2800.00), (val_l, 2800.00)]},
        {'cat': cat_clothing, 'name': 'Comfort-First Jogger Pants', 'slug': 'comfort-jogger-pants', 'desc': 'Ultra-soft fleece jogger pants with a relaxed fit, perfect for lounging or casual outings.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/0c/45/9d/0c459d3e9e2a51c33888edbfd5455e50.jpg', 'variants': [(val_s, 1600.00), (val_m, 1600.00)]},
        {'cat': cat_clothing, 'name': 'Fisherman Beanie Hat', 'slug': 'fisherman-beanie-hat', 'desc': 'A soft, ribbed-knit beanie hat for a stylish and cozy finishing touch to any look.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/11/13/9c/11139c2b45867e8223724a40cee6f6fd.jpg', 'variants': [(None, 650.00)]},
    
        # == FOOTWEAR ==
        {'cat': cat_women_shoes, 'name': 'Autumn Casual Board Shoes', 'slug': 'autumn-board-shoes', 'desc': 'Unisex-style, breathable board shoes inspired by 2025 Wenzhou designs.', 'tags': [tag_women, tag_new], 'img': 'https://i.pinimg.com/1200x/da/2b/86/da2b86ca749f7cd3c3d09baf7b0067fc.jpg', 'variants': [(val_ss_38, 830.74), (val_ss_39, 830.74)]},
        {'cat': cat_women_shoes, 'name': 'Elegant Heeled Sandals', 'slug': 'heeled-sandals', 'desc': 'A pair of elegant sandals with a comfortable block heel, perfect for formal events and evening outings.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/d9/31/cf/d931cfec0d61f5c63882b515ca71407a.jpg', 'variants': [(val_ss_38, 1400.00), (val_ss_39, 1400.00)]},
        {'cat': cat_women_shoes, 'name': 'Comfort Slip-On Flats', 'slug': 'slip-on-flats', 'desc': 'The perfect everyday shoe, combining chic style with all-day comfort. Easy to wear and versatile.', 'tags': [tag_women, tag_bestseller], 'img': 'https://i.pinimg.com/736x/de/a4/3b/dea43be9df9fb8a80b552a8c07f2a8db.jpg', 'variants': [(val_ss_38, 950.00), (val_ss_39, 950.00)]},
        {'cat': cat_women_shoes, 'name': 'Classic White Canvas Sneakers', 'slug': 'women-white-canvas-sneakers', 'desc': 'A timeless wardrobe staple. These canvas sneakers offer a clean, crisp look that pairs with anything.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/f3/a5/7c/f3a57cda5b4675ac6b1364e34244a349.jpg', 'variants': [(val_ss_38, 1100.00), (val_ss_39, 1100.00), (val_ss_37, 1100.00)]},
        {'cat': cat_women_shoes, 'name': 'Chic Ankle Boots', 'slug': 'chic-ankle-boots', 'desc': 'Stylish and versatile ankle boots with a low heel, perfect for adding an edge to any outfit.', 'tags': [tag_women, tag_new], 'img': 'https://i.pinimg.com/736x/7b/e4/9c/7be49cc38c756772093e084be2b2f7f8.jpg', 'variants': [(val_ss_38, 2500.00), (val_ss_39, 2500.00)]},
        {'cat': cat_men_shoes, 'name': 'Urban Explorer Sneakers', 'slug': 'urban-sneakers', 'desc': 'Versatile and comfortable unisex sneakers, sourced from Wenzhou King-Footwear.', 'tags': [tag_men, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/0d/aa/e9/0daae9d9134677506296ff4bcaa89fd5.jpg', 'variants': [(val_ss_41, 770.00), (val_ss_42, 770.00)]},
        {'cat': cat_men_shoes, 'name': 'Handcrafted Leather Boots', 'slug': 'leather-boots', 'desc': 'Durable, handcrafted leather boots that combine timeless style with rugged, all-weather functionality.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/f2/b8/ae/f2b8aebdddfd18da1f1fd625c848d3bd.jpg', 'variants': [(val_ss_41, 2800.00), (val_ss_42, 2800.00)]},
        {'cat': cat_men_shoes, 'name': 'Suede Driving Loafers', 'slug': 'driving-loafers', 'desc': 'Sophisticated suede loafers designed for a smart-casual look and ultimate driving comfort.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/736x/f3/81/11/f3811147f4eafa86aa089b52f0c49b08.jpg', 'variants': [(val_ss_41, 2100.00), (val_ss_42, 2100.00)]},
        {'cat': cat_men_shoes, 'name': 'Classic Leather Oxford Shoes', 'slug': 'classic-oxford-shoes', 'desc': 'The quintessential dress shoe. Perfect for formal occasions, business meetings, and professional events.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/7b/58/ef/7b58efdb0579820d7c3651831e429bd5.jpg', 'variants': [(val_ss_41, 3200.00), (val_ss_42, 3200.00)]},
        {'cat': cat_men_shoes, 'name': 'Casual Canvas Espadrilles', 'slug': 'canvas-espadrilles', 'desc': 'Lightweight and breathable canvas espadrilles, the perfect footwear for summer and beach holidays.', 'tags': [tag_men, tag_new], 'img': 'https://i.pinimg.com/1200x/2b/16/7f/2b167ffc710591055f183a96cc6bf0ff.jpg', 'variants': [(val_ss_41, 1200.00), (val_ss_42, 1200.00)]},
        # == BEAUTY PRODUCTS ==
        {'cat': cat_skincare, 'name': 'Rejuvenating Vitamin C Serum', 'slug': 'vitamin-c-serum', 'desc': 'Brightens and revitalizes skin with a potent blend of antioxidants.', 'tags': [tag_unisex, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/74/eb/1d/74eb1d724817aa18805654c59f4d0999.jpg', 'variants': [(val_v_50, 1200.00), (val_v_100, 2000.00)]},
        {'cat': cat_skincare, 'name': 'Hydrating Aloe Vera Gel', 'slug': 'aloe-vera-gel', 'desc': 'Soothes and hydrates skin with pure aloe vera extract.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/86/65/8f/86658fd5d0884577108df145831e2063.jpg', 'variants': [(val_v_100, 800.00)]},
        {'cat': cat_skincare, 'name': 'Organic Green Tea Face Mask', 'slug': 'green-tea-mask', 'desc': 'Detoxifying face mask enriched with organic green tea.', 'tags': [tag_unisex, tag_eco], 'img': 'https://i.pinimg.com/736x/31/39/85/3139856f1608437be1bfd4e84a379168.jpg', 'variants': [(val_v_50, 950.00)]},
        {'cat': cat_skincare, 'name': 'Revitalizing Eye Cream', 'slug': 'eye-cream', 'desc': 'Reduces dark circles and puffiness for a refreshed look.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/59/ee/59/59ee596f2dc09ab8acb8befb33d25cf4.jpg', 'variants': [(val_v_250, 1500.00)]},
        {'cat': cat_haircare, 'name': 'Nourishing Argan Oil Shampoo', 'slug': 'argan-oil-shampoo', 'desc': 'Infused with argan oil to nourish and strengthen hair.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/6e/75/ec/6e75ecefeaa6d536374ae939295c721d.jpg', 'variants': [(val_v_250, 1100.00)]},
        {'cat': cat_haircare, 'name': 'Moisturizing Coconut Conditioner', 'slug': 'coconut-conditioner', 'desc': 'Deeply hydrates and detangles hair with coconut extract.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/40/39/00/403900d7fcfc88dc7db4453123916cb9.jpg', 'variants': [(val_v_250, 950.00)]},
        {'cat': cat_haircare, 'name': 'Revitalizing Hair Growth Serum', 'slug': 'hair-growth-serum', 'desc': 'Stimulates hair growth with a blend of natural oils.', 'tags': [tag_unisex, tag_bestseller], 'img': 'https://i.pinimg.com/736x/68/ab/b6/68abb66cb0e6ab720a151f23be26015e.jpg', 'variants': [(val_v_50, 1500.00)]},
        {'cat': cat_skincare, 'name': 'Synogal 7-Color LED Therapy Mask', 'slug': 'synogal-led-mask', 'desc': 'A home-use phototherapy mask for skin whitening and rejuvenation from Guangzhou.', 'tags': [tag_unisex, tag_new], 'img': 'https://i.pinimg.com/1200x/ad/62/9b/ad629b81c3fa91e2194e5e6234026fb8.jpg', 'variants': [(None, 3268.45)]},
        {'cat': cat_skincare, 'name': 'Hydrating Hyaluronic Acid Serum', 'slug': 'hydrating-serum', 'desc': 'A powerful serum to lock in moisture for a youthful glow. For all skin types.', 'tags': [tag_unisex, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/9e/9c/6f/9e9c6f8bf6f4324fda17f6b64d07801d.jpg', 'variants': [(val_v_50, 1100.00), (val_v_100, 1900.00)]},
        {'cat': cat_skincare, 'name': "Men's Revitalizing Face Wash", 'slug': 'men-face-wash', 'desc': 'A daily cleanser designed to remove grime and energize men\'s skin.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/736x/37/ae/77/37ae7758a52e6ddb9bc8272e28d5e232.jpg', 'variants': [(val_v_100, 950.00)]},
        {'cat': cat_haircare, 'name': 'Argan Oil Repairing Hair Mask', 'slug': 'argan-hair-mask', 'desc': 'Deeply conditions and restores shine to dry or damaged hair.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/736x/ae/2e/ba/ae2ebaf561b6f3fb0547b149319aa5fe.jpg', 'variants': [(val_v_250, 1300.00)]},
        {'cat': cat_haircare, 'name': "Men's Firm Hold Styling Pomade", 'slug': 'men-pomade', 'desc': 'For a sharp, classic look with a strong hold and matte finish.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/0e/35/79/0e357995c9f25432c237b8e567850cd6.jpg', 'variants': [(val_v_100, 850.00)]},
        {'cat': cat_haircare, 'name': 'Tea Tree Scalp Treatment Shampoo', 'slug': 'tea-tree-shampoo', 'desc': 'A clarifying shampoo that soothes the scalp and removes buildup. For all.', 'tags': [tag_unisex, tag_eco], 'img': 'https://i.pinimg.com/1200x/9a/97/bd/9a97bd061694762616593fd02395b5e3.jpg', 'variants': [(val_v_250, 1050.00)]},
    
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