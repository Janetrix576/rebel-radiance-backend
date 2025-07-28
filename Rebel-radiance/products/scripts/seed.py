from django.db import transaction
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beautyshop.settings')
django.setup()

from products.models import Category, Tag, Attribute, AttributeValue, Product, ProductVariant, ProductImage

def run():
    try:
        with transaction.atomic():
            print("Deleting old data...")
            ProductImage.objects.all().delete()
            ProductVariant.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            AttributeValue.objects.all().delete()
            Attribute.objects.all().delete()
            print("Old data has been cleared.")

            print("Seeding new beauty products...")
            tag_new, _ = Tag.objects.get_or_create(name="New Arrival")
            tag_unisex, _ = Tag.objects.get_or_create(name="Unisex")
            tag_men, _ = Tag.objects.get_or_create(name="For Men")
            tag_women, _ = Tag.objects.get_or_create(name="For Women")
            tag_bestseller, _ = Tag.objects.get_or_create(name="Bestseller")
            tag_eco, _ = Tag.objects.get_or_create(name="Eco-Friendly")
            tag_vegan, _ = Tag.objects.get_or_create(name="Vegan")

            attr_volume, _ = Attribute.objects.get_or_create(name="Volume")
            val_v_30, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="30ml")
            val_v_50, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="50ml")
            val_v_100, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="100ml")
            val_v_150, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="150ml")
            val_v_250, _ = AttributeValue.objects.get_or_create(attribute=attr_volume, value="250ml")

            attr_scent, _ = Attribute.objects.get_or_create(name="Scent Profile")
            val_s_woody, _ = AttributeValue.objects.get_or_create(attribute=attr_scent, value="Woody & Spicy")
            val_s_floral, _ = AttributeValue.objects.get_or_create(attribute=attr_scent, value="Floral & Sweet")
            val_s_fresh, _ = AttributeValue.objects.get_or_create(attribute=attr_scent, value="Fresh & Citrus")

            cat_beauty, _ = Category.objects.get_or_create(name="Beauty", defaults={'slug': 'beauty'})
            cat_skincare, _ = Category.objects.get_or_create(name="Skincare", defaults={'slug': 'skincare', 'parent': cat_beauty})
            cat_haircare, _ = Category.objects.get_or_create(name="Haircare", defaults={'slug': 'haircare', 'parent': cat_beauty})
            cat_fragrance, _ = Category.objects.get_or_create(name="Fragrance", defaults={'slug': 'fragrance', 'parent': cat_beauty})
            cat_grooming, _ = Category.objects.get_or_create(name="Grooming", defaults={'slug': 'grooming', 'parent': cat_beauty})

            product_definitions = [
                {'cat': cat_skincare, 'name': 'Rejuvenating Vitamin C Serum', 'slug': 'vitamin-c-serum', 'desc': 'Brightens and revitalizes skin with a potent blend of antioxidants.', 'tags': [tag_unisex, tag_bestseller], 'img': 'https://i.pinimg.com/736x/c6/4c/b6/c64cb632db7f82cb6d21e423b5fd7455.jpg', 'variants': [(val_v_30, 1200.00), (val_v_50, 1800.00)]},
                {'cat': cat_skincare, 'name': 'Hydrating Aloe Vera Gel', 'slug': 'aloe-vera-gel', 'desc': 'Soothes and hydrates skin with pure aloe vera extract.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/50/fe/e5/50fee561ec2d261678e7adce6b19903d.jpg', 'variants': [(val_v_100, 800.00)]},
                {'cat': cat_skincare, 'name': 'Organic Green Tea Face Mask', 'slug': 'green-tea-mask', 'desc': 'Detoxifying face mask enriched with organic green tea.', 'tags': [tag_unisex, tag_eco], 'img': 'https://i.pinimg.com/736x/40/13/fe/4013fe55ae7b6b890fb6005132d40edf.jpg', 'variants': [(val_v_50, 950.00)]},
                {'cat': cat_skincare, 'name': "Men's Revitalizing Face Wash", 'slug': 'men-face-wash', 'desc': 'A daily cleanser designed to remove grime and energize men\'s skin.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/a4/b2/1a/a4b21a65219ac0d12e984ff0f42ededc.jpg', 'variants': [(val_v_150, 950.00)]},
                {'cat': cat_skincare, 'name': 'Gentle Micellar Cleansing Water', 'slug': 'micellar-water', 'desc': 'Removes makeup and impurities without stripping the skin. Suitable for all skin types.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/736x/5e/f2/51/5ef25145f9caec215c447bfb003c2487.jpg', 'variants': [(val_v_250, 1150.00)]},
                {'cat': cat_skincare, 'name': 'Anti-Aging Retinol Cream', 'slug': 'retinol-cream', 'desc': 'A powerful night cream formulated to reduce the appearance of fine lines and wrinkles.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/bd/7a/3d/bd7a3d14b3c40f060298b2ebb3504a7f.jpg', 'variants': [(val_v_50, 2500.00)]},
                {'cat': cat_skincare, 'name': 'Clarifying Clay Mask', 'slug': 'clay-mask', 'desc': 'Absorbs excess oil and impurities to leave skin feeling clean and refreshed.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/40/3b/5c/403b5c434d102a3dab7018b71c90005a.jpg', 'variants': [(val_v_100, 1300.00)]},
                {'cat': cat_skincare, 'name': 'Daily Moisturizer with SPF 30', 'slug': 'spf-moisturizer', 'desc': 'A lightweight daily moisturizer that hydrates and protects skin from sun damage.', 'tags': [tag_unisex, tag_bestseller], 'img': 'https://i.pinimg.com/736x/79/e8/9f/79e89f4959df3ac5aae5b6c7f7d10519.jpg', 'variants': [(val_v_50, 1600.00)]},
                {'cat': cat_skincare, 'name': 'Soothing Rosewater Facial Mist', 'slug': 'rosewater-mist', 'desc': 'A refreshing facial mist to hydrate and tone the skin throughout the day.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/a1/a1/56/a1a156d5fb510e17acab97b7b547aab6.jpg', 'variants': [(val_v_100, 750.00)]},
                {'cat': cat_skincare, 'name': 'Synogal 7-Color LED Therapy Mask', 'slug': 'synogal-led-mask', 'desc': 'A home-use phototherapy mask for skin whitening and rejuvenation.', 'tags': [tag_unisex, tag_new], 'img': 'https://i.pinimg.com/1200x/ad/62/9b/ad629b81c3fa91e2194e5e6234026fb8.jpg', 'variants': [(None, 3268.45)]},
                {'cat': cat_haircare, 'name': 'Nourishing Argan Oil Shampoo', 'slug': 'argan-oil-shampoo', 'desc': 'Infused with argan oil to nourish and strengthen hair.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/fa/fd/c4/fafdc47e0f805757f07273208551e91a.jpg', 'variants': [(val_v_250, 1100.00)]},
                {'cat': cat_haircare, 'name': 'Argan Oil Repairing Hair Mask', 'slug': 'argan-hair-mask', 'desc': 'Deeply conditions and restores shine to dry or damaged hair.', 'tags': [tag_women], 'img': 'https://i.pinimg.com/1200x/a9/e0/ab/a9e0ab88c3d09139832f5503976c714a.jpg', 'variants': [(val_v_250, 1300.00)]},
                {'cat': cat_haircare, 'name': "Men's Firm Hold Styling Pomade", 'slug': 'men-pomade', 'desc': 'For a sharp, classic look with a strong hold and matte finish.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/736x/e1/2e/bc/e12ebc1c8ff4e587abc6b343857f9305.jpg', 'variants': [(val_v_100, 850.00)]},
                {'cat': cat_haircare, 'name': 'Volumizing Dry Shampoo', 'slug': 'dry-shampoo', 'desc': 'Instantly refreshes hair and adds volume between washes.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/23/c0/80/23c080001b2d6773875fcdb1ccb71225.jpg', 'variants': [(val_v_150, 900.00)]},
                {'cat': cat_haircare, 'name': 'Curl Defining Cream', 'slug': 'curl-cream', 'desc': 'Enhances natural curls, reduces frizz, and adds definition without stiffness.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/51/94/47/519447b3fab7db93b92f3eff2f4c8bdb.jpg', 'variants': [(val_v_150, 1250.00)]},
                {'cat': cat_haircare, 'name': 'Heat Protectant Spray', 'slug': 'heat-protectant', 'desc': 'Shields hair from heat damage caused by styling tools.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/ba/a2/34/baa23408308095b665daa16d992b163f.jpg', 'variants': [(val_v_100, 980.00)]},
                {'cat': cat_haircare, 'name': 'Tea Tree Scalp Treatment', 'slug': 'tea-tree-scalp', 'desc': 'A soothing treatment to relieve dry, itchy scalp and reduce dandruff.', 'tags': [tag_unisex, tag_eco], 'img': 'https://i.pinimg.com/1200x/35/c1/32/35c1328cf0e1a1772bc7dce493f75c0a.jpg', 'variants': [(val_v_50, 1400.00)]},
                {'cat': cat_haircare, 'name': "Men's 2-in-1 Shampoo & Conditioner", 'slug': 'men-2-in-1', 'desc': 'A convenient, effective formula that cleanses and conditions in one step.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/1200x/7e/01/96/7e0196fd95925e560a412ad11e98dc13.jpg', 'variants': [(val_v_250, 1000.00)]},
                {'cat': cat_fragrance, 'name': 'Noir Enigma Eau de Parfum', 'slug': 'noir-enigma-perfume', 'desc': 'A bold and mysterious scent for the modern man.', 'tags': [tag_men, tag_new], 'img': 'https://i.pinimg.com/736x/08/77/d0/0877d0fc1d193f3174dfc05c30d3cdf1.jpg', 'variants': [(val_v_50, 4500.00), (val_v_100, 6200.00)]},
                {'cat': cat_fragrance, 'name': 'Velvet Bloom Eau de Parfum', 'slug': 'velvet-bloom-perfume', 'desc': 'An elegant and floral fragrance for women.', 'tags': [tag_women, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/10/1e/b2/101eb25484d17040e04d7d6ecc1437d8.jpg', 'variants': [(val_v_50, 4800.00), (val_v_100, 6500.00)]},
                {'cat': cat_fragrance, 'name': 'Ocean Breeze Eau de Toilette', 'slug': 'ocean-breeze-perfume', 'desc': 'A fresh, aquatic unisex scent that captures the essence of a sea breeze.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/ee/4c/20/ee4c20fac4d9635536becb08869dcb83.jpg', 'variants': [(val_v_100, 5500.00)]},
                {'cat': cat_fragrance, 'name': 'Citrus Grove Cologne', 'slug': 'citrus-cologne', 'desc': 'An uplifting and zesty citrus fragrance, perfect for daytime wear.', 'tags': [tag_unisex, tag_new], 'img': 'https://i.pinimg.com/736x/bb/67/56/bb6756030d39c7d169afd7bcc34705fa.jpg', 'variants': [(val_v_100, 5200.00)]},
                {'cat': cat_fragrance, 'name': 'Midnight Oud Perfume Oil', 'slug': 'midnight-oud-oil', 'desc': 'A rich, concentrated perfume oil with deep notes of oud and amber.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/736x/5a/e9/bb/5ae9bb99bb49a5265ccbbfa40cf2fb42.jpg', 'variants': [(val_v_30, 3800.00)]},
                {'cat': cat_grooming, 'name': 'Premium Beard Oil', 'slug': 'premium-beard-oil', 'desc': 'Softens and conditions the beard while moisturizing the skin underneath.', 'tags': [tag_men, tag_bestseller], 'img': 'https://i.pinimg.com/1200x/20/92/cd/2092cd690bba41305b9d144550118490.jpg', 'variants': [(val_v_30, 1500.00)]},
                {'cat': cat_grooming, 'name': 'Luxury Shaving Cream', 'slug': 'shaving-cream', 'desc': 'A rich, lathering cream for a smooth, comfortable shave.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/736x/e9/14/e5/e914e56bacd474e0a4486ca2f5f079b0.jpg', 'variants': [(val_v_150, 1200.00)]},
                {'cat': cat_grooming, 'name': 'Aftershave Balm', 'slug': 'aftershave-balm', 'desc': 'A soothing, alcohol-free balm to calm and hydrate skin post-shave.', 'tags': [tag_men], 'img': 'https://i.pinimg.com/736x/9d/71/c6/9d71c6a2259a5ef5f9ecbf191ad74b48.jpg', 'variants': [(val_v_100, 1350.00)]},
                {'cat': cat_grooming, 'name': 'Exfoliating Body Scrub', 'slug': 'body-scrub', 'desc': 'A refreshing body scrub with natural exfoliants to polish away dead skin cells.', 'tags': [tag_unisex, tag_vegan], 'img': 'https://i.pinimg.com/1200x/c9/ce/7f/c9ce7f33ae214c889150bb65a9cc01dc.jpg', 'variants': [(val_v_250, 1600.00)]},
                {'cat': cat_grooming, 'name': 'Nourishing Body Lotion', 'slug': 'body-lotion', 'desc': 'A fast-absorbing lotion that provides long-lasting hydration for smooth, soft skin.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/04/a9/bf/04a9bfb2d6bd93b5f5c20273f6071b49.jpg', 'variants': [(val_v_250, 1400.00)]},
                {'cat': cat_grooming, 'name': 'Charcoal Detox Bar Soap', 'slug': 'charcoal-soap', 'desc': 'A purifying bar soap made with activated charcoal to draw out impurities.', 'tags': [tag_unisex, tag_eco], 'img': 'https://i.pinimg.com/736x/eb/e6/5d/ebe65dbc3cf3407c5ef8cecbdc371216.jpg', 'variants': [(None, 700.00)]},
                {'cat': cat_grooming, 'name': 'Precision Tweezers', 'slug': 'tweezers', 'desc': 'Professional-grade stainless steel tweezers for precise grooming.', 'tags': [tag_unisex], 'img': 'https://i.pinimg.com/1200x/d6/6c/c5/d66cc5f184cefd1e54263cde7e1962db.jpg', 'variants': [(None, 500.00)]},
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
                    ProductImage.objects.create(product=product, image_url=p_data['img'], alt_text=f"Image of {product.name}")

                    for variant_data in p_data['variants']:
                        price = variant_data[1]
                        variant = ProductVariant.objects.create(product=product, price=price, stock=random.randint(5, 50))
                        
                        attr_val = variant_data[0]
                        if attr_val:
                            variant.attributes.add(attr_val)
                else:
                    print(f"  - Product already exists: {p_data['name']}")


            print("\nSeeding complete!")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        raise e