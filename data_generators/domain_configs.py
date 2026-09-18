"""
Outlook360 - Universal Domain Catalog Configurations (Indian Rupee ₹ / INR Edition)
Defines catalogs, categories, pricing, lead times, and co-purchase affinities
for 6 distinct retail and service industries localized in Indian Rupees.
"""
from typing import Dict, Any, List

DOMAIN_CATALOGS: Dict[str, Dict[str, Any]] = {
    "supermarket": {
        "domain_key": "supermarket",
        "business_name": "FreshPulse Supermarket & Daily Essentials",
        "tagline": "Fresh Food, Daily Groceries & FMCG Essentials",
        "currency": "₹",
        "tax_rate": 0.05,
        "categories": [
            {"name": "Fresh Produce", "department": "Perishables", "tax_slab": 0.00},
            {"name": "Dairy & Bakery", "department": "Perishables", "tax_slab": 0.05},
            {"name": "Beverages & Tea", "department": "FMCG", "tax_slab": 0.05},
            {"name": "Snacks & Confectionery", "department": "FMCG", "tax_slab": 0.12},
            {"name": "Household & Cleaning", "department": "Non-Food", "tax_slab": 0.18},
            {"name": "Personal Care", "department": "Non-Food", "tax_slab": 0.18}
        ],
        "products": [
            # Fresh Produce
            {"sku": "GROC-PROD-001", "name": "Shimla Red Apples (1kg)", "category": "Fresh Produce", "cost": 120.00, "price": 180.00, "stock": 80, "reorder": 20, "lead_time": 2, "shelf_life": 14},
            {"sku": "GROC-PROD-002", "name": "Robusta Bananas (1 Dozen)", "category": "Fresh Produce", "cost": 40.00, "price": 60.00, "stock": 100, "reorder": 25, "lead_time": 1, "shelf_life": 6},
            {"sku": "GROC-PROD-003", "name": "Farm Fresh Tomatoes (1kg)", "category": "Fresh Produce", "cost": 25.00, "price": 40.00, "stock": 90, "reorder": 20, "lead_time": 1, "shelf_life": 8},
            {"sku": "GROC-PROD-004", "name": "Fresh Palak / Spinach (250g)", "category": "Fresh Produce", "cost": 15.00, "price": 25.00, "stock": 60, "reorder": 15, "lead_time": 1, "shelf_life": 4},
            {"sku": "GROC-PROD-005", "name": "Nashik Red Onions (2kg Bag)", "category": "Fresh Produce", "cost": 45.00, "price": 70.00, "stock": 85, "reorder": 20, "lead_time": 2, "shelf_life": 30},
            
            # Dairy & Bakery
            {"sku": "GROC-DAIR-001", "name": "Amul Gold Full Cream Milk (1L)", "category": "Dairy & Bakery", "cost": 55.00, "price": 66.00, "stock": 110, "reorder": 30, "lead_time": 1, "shelf_life": 4},
            {"sku": "GROC-DAIR-002", "name": "Britannia Whole Wheat Bread (400g)", "category": "Dairy & Bakery", "cost": 32.00, "price": 45.00, "stock": 70, "reorder": 20, "lead_time": 1, "shelf_life": 4},
            {"sku": "GROC-DAIR-003", "name": "Amul Salted Butter (100g)", "category": "Dairy & Bakery", "cost": 46.00, "price": 58.00, "stock": 80, "reorder": 20, "lead_time": 2, "shelf_life": 90},
            {"sku": "GROC-DAIR-004", "name": "Mother Dairy Fresh Paneer (200g)", "category": "Dairy & Bakery", "cost": 72.00, "price": 95.00, "stock": 65, "reorder": 15, "lead_time": 1, "shelf_life": 15},
            {"sku": "GROC-DAIR-005", "name": "Amul Processed Cheese Block (200g)", "category": "Dairy & Bakery", "cost": 98.00, "price": 135.00, "stock": 60, "reorder": 15, "lead_time": 2, "shelf_life": 180},
            {"sku": "GROC-DAIR-006", "name": "Farm Fresh White Eggs (6pk)", "category": "Dairy & Bakery", "cost": 34.00, "price": 48.00, "stock": 95, "reorder": 25, "lead_time": 1, "shelf_life": 14},

            # Beverages & Tea
            {"sku": "GROC-BEV-001", "name": "Tata Tea Gold (500g)", "category": "Beverages & Tea", "cost": 210.00, "price": 280.00, "stock": 60, "reorder": 15, "lead_time": 3, "shelf_life": 365},
            {"sku": "GROC-BEV-002", "name": "Nescafe Classic Coffee (100g Jar)", "category": "Beverages & Tea", "cost": 165.00, "price": 220.00, "stock": 50, "reorder": 12, "lead_time": 3, "shelf_life": 365},
            {"sku": "GROC-BEV-003", "name": "Real Mixed Fruit Juice (1L)", "category": "Beverages & Tea", "cost": 82.00, "price": 115.00, "stock": 70, "reorder": 18, "lead_time": 2, "shelf_life": 180},

            # Snacks & Confectionery
            {"sku": "GROC-SNAK-001", "name": "Lay's India's Magic Masala (90g)", "category": "Snacks & Confectionery", "cost": 22.00, "price": 30.00, "stock": 140, "reorder": 30, "lead_time": 2, "shelf_life": 120},
            {"sku": "GROC-SNAK-002", "name": "Cadbury Dairy Milk Silk (150g)", "category": "Snacks & Confectionery", "cost": 130.00, "price": 175.00, "stock": 75, "reorder": 18, "lead_time": 3, "shelf_life": 240},
            {"sku": "GROC-SNAK-003", "name": "Haldiram's Aloo Bhujia (400g)", "category": "Snacks & Confectionery", "cost": 92.00, "price": 125.00, "stock": 65, "reorder": 15, "lead_time": 3, "shelf_life": 180},
            {"sku": "GROC-SNAK-004", "name": "Maggi 2-Minute Masala Noodles (4pk)", "category": "Snacks & Confectionery", "cost": 42.00, "price": 56.00, "stock": 120, "reorder": 30, "lead_time": 2, "shelf_life": 240},

            # Household & Cleaning
            {"sku": "GROC-HOUS-001", "name": "Surf Excel Matic Front Load (2kg)", "category": "Household & Cleaning", "cost": 310.00, "price": 395.00, "stock": 40, "reorder": 10, "lead_time": 4, "shelf_life": 730},
            {"sku": "GROC-HOUS-002", "name": "Vim Dishwash Gel Lemon (750ml)", "category": "Household & Cleaning", "cost": 115.00, "price": 155.00, "stock": 65, "reorder": 15, "lead_time": 3, "shelf_life": 730},
            {"sku": "GROC-HOUS-003", "name": "Lizol Disinfectant Floor Cleaner (1L)", "category": "Household & Cleaning", "cost": 140.00, "price": 185.00, "stock": 55, "reorder": 12, "lead_time": 3, "shelf_life": 730},

            # Personal Care
            {"sku": "GROC-PERS-001", "name": "Dettol Original Germ Protection Soap (3x125g)", "category": "Personal Care", "cost": 105.00, "price": 140.00, "stock": 70, "reorder": 18, "lead_time": 3, "shelf_life": 730},
            {"sku": "GROC-PERS-002", "name": "Colgate Total Active Toothpaste (150g)", "category": "Personal Care", "cost": 90.00, "price": 120.00, "stock": 80, "reorder": 20, "lead_time": 3, "shelf_life": 730}
        ],
        "affinity_bundles": [
            ("Amul Gold Full Cream Milk (1L)", "Britannia Whole Wheat Bread (400g)", "Amul Salted Butter (100g)"),
            ("Tata Tea Gold (500g)", "Amul Gold Full Cream Milk (1L)", "Cadbury Dairy Milk Silk (150g)"),
            ("Maggi 2-Minute Masala Noodles (4pk)", "Lay's India's Magic Masala (90g)"),
            ("Mother Dairy Fresh Paneer (200g)", "Farm Fresh Tomatoes (1kg)", "Nashik Red Onions (2kg Bag)"),
            ("Shimla Red Apples (1kg)", "Robusta Bananas (1 Dozen)")
        ]
    },

    "pharmacy": {
        "domain_key": "pharmacy",
        "business_name": "MediPulse Pharmacy & Healthcare",
        "tagline": "Prescription Drugs, Generic Care & Diagnostic Devices",
        "currency": "₹",
        "tax_rate": 0.05,
        "categories": [
            {"name": "Prescription Rx", "department": "Pharmacy", "tax_slab": 0.05},
            {"name": "OTC Cold & Pain", "department": "Healthcare", "tax_slab": 0.05},
            {"name": "Vitamins & Supplements", "department": "Wellness", "tax_slab": 0.12},
            {"name": "First Aid & Antiseptics", "department": "Medical", "tax_slab": 0.05},
            {"name": "Medical Devices & Monitors", "department": "Diagnostics", "tax_slab": 0.12},
            {"name": "Derma & Skincare", "department": "Personal Health", "tax_slab": 0.18}
        ],
        "products": [
            {"sku": "PHAR-PRES-001", "name": "Amoxicillin 500mg (10 Caps)", "category": "Prescription Rx", "cost": 65.00, "price": 95.00, "stock": 80, "reorder": 20, "lead_time": 2, "shelf_life": 540},
            {"sku": "PHAR-PRES-002", "name": "Atorvastatin 10mg (15 Tabs)", "category": "Prescription Rx", "cost": 95.00, "price": 140.00, "stock": 70, "reorder": 18, "lead_time": 3, "shelf_life": 730},
            {"sku": "PHAR-PRES-003", "name": "Metformin 500mg SR (20 Tabs)", "category": "Prescription Rx", "cost": 28.00, "price": 45.00, "stock": 90, "reorder": 25, "lead_time": 2, "shelf_life": 730},
            {"sku": "PHAR-PRES-004", "name": "Pantocid 40mg (15 Tabs)", "category": "Prescription Rx", "cost": 115.00, "price": 165.00, "stock": 65, "reorder": 15, "lead_time": 2, "shelf_life": 730},

            {"sku": "PHAR-PAIN-001", "name": "Dolo 650mg Paracetamol (15 Tabs)", "category": "OTC Cold & Pain", "cost": 22.00, "price": 32.00, "stock": 250, "reorder": 60, "lead_time": 1, "shelf_life": 730},
            {"sku": "PHAR-PAIN-002", "name": "Combiflam Pain Relief (20 Tabs)", "category": "OTC Cold & Pain", "cost": 34.00, "price": 48.00, "stock": 160, "reorder": 40, "lead_time": 1, "shelf_life": 730},
            {"sku": "PHAR-PAIN-003", "name": "Benadryl Cough Syrup (100ml)", "category": "OTC Cold & Pain", "cost": 85.00, "price": 115.00, "stock": 90, "reorder": 20, "lead_time": 2, "shelf_life": 365},
            {"sku": "PHAR-PAIN-004", "name": "Cetirizine 10mg Relief (10 Tabs)", "category": "OTC Cold & Pain", "cost": 18.00, "price": 28.00, "stock": 120, "reorder": 30, "lead_time": 2, "shelf_life": 730},

            {"sku": "PHAR-VITA-001", "name": "Limcee Vitamin C 500mg (15 Chewables)", "category": "Vitamins & Supplements", "cost": 16.00, "price": 25.00, "stock": 180, "reorder": 40, "lead_time": 2, "shelf_life": 540},
            {"sku": "PHAR-VITA-002", "name": "Becosules Performance Capsules (30 Caps)", "category": "Vitamins & Supplements", "cost": 110.00, "price": 160.00, "stock": 80, "reorder": 20, "lead_time": 2, "shelf_life": 730},
            {"sku": "PHAR-VITA-003", "name": "Seven Seas Cod Liver Oil (100 Caps)", "category": "Vitamins & Supplements", "cost": 240.00, "price": 340.00, "stock": 60, "reorder": 15, "lead_time": 3, "shelf_life": 730},

            {"sku": "PHAR-FAID-001", "name": "Hansaplast Washproof Bandages (20pk)", "category": "First Aid & Antiseptics", "cost": 30.00, "price": 45.00, "stock": 130, "reorder": 30, "lead_time": 2, "shelf_life": 1095},
            {"sku": "PHAR-FAID-002", "name": "Dettol Antiseptic Liquid (250ml)", "category": "First Aid & Antiseptics", "cost": 98.00, "price": 135.00, "stock": 85, "reorder": 20, "lead_time": 2, "shelf_life": 730},
            {"sku": "PHAR-FAID-003", "name": "Cotton Gauze Bandage Roll (5m)", "category": "First Aid & Antiseptics", "cost": 18.00, "price": 30.00, "stock": 90, "reorder": 20, "lead_time": 2, "shelf_life": 1095},

            {"sku": "PHAR-DEVC-001", "name": "Dr. Morepen Digital Thermometer", "category": "Medical Devices & Monitors", "cost": 160.00, "price": 249.00, "stock": 45, "reorder": 10, "lead_time": 4, "shelf_life": 1825},
            {"sku": "PHAR-DEVC-002", "name": "Omron Automatic Blood Pressure Monitor", "category": "Medical Devices & Monitors", "cost": 1350.00, "price": 1850.00, "stock": 25, "reorder": 6, "lead_time": 5, "shelf_life": 1825},
            {"sku": "PHAR-DEVC-003", "name": "Fingertip Pulse Oximeter", "category": "Medical Devices & Monitors", "cost": 520.00, "price": 799.00, "stock": 35, "reorder": 8, "lead_time": 4, "shelf_life": 1825},

            {"sku": "PHAR-SKIN-001", "name": "Cetaphil Gentle Skin Cleanser (125ml)", "category": "Derma & Skincare", "cost": 240.00, "price": 330.00, "stock": 50, "reorder": 12, "lead_time": 3, "shelf_life": 730},
            {"sku": "PHAR-SKIN-002", "name": "La Shield Sunscreen Gel SPF 40 (50g)", "category": "Derma & Skincare", "cost": 290.00, "price": 420.00, "stock": 55, "reorder": 12, "lead_time": 3, "shelf_life": 540}
        ],
        "affinity_bundles": [
            ("Dolo 650mg Paracetamol (15 Tabs)", "Benadryl Cough Syrup (100ml)", "Limcee Vitamin C 500mg (15 Chewables)"),
            ("Hansaplast Washproof Bandages (20pk)", "Dettol Antiseptic Liquid (250ml)", "Cotton Gauze Bandage Roll (5m)"),
            ("Omron Automatic Blood Pressure Monitor", "Atorvastatin 10mg (15 Tabs)"),
            ("Dr. Morepen Digital Thermometer", "Dolo 650mg Paracetamol (15 Tabs)", "Fingertip Pulse Oximeter")
        ]
    },

    "restaurant": {
        "domain_key": "restaurant",
        "business_name": "GourmetPulse Bistro & Cafe",
        "tagline": "Artisanal Kitchen, North Indian Curries & Specialty Beverages",
        "currency": "₹",
        "tax_rate": 0.05,
        "categories": [
            {"name": "Starters & Appetizers", "department": "Kitchen", "tax_slab": 0.05},
            {"name": "Woodfired Pizzas & Pastas", "department": "Kitchen", "tax_slab": 0.05},
            {"name": "Main Course & Curries", "department": "Kitchen", "tax_slab": 0.05},
            {"name": "Breads & Rice Combos", "department": "Kitchen", "tax_slab": 0.05},
            {"name": "Beverages & Mocktails", "department": "Barista", "tax_slab": 0.12},
            {"name": "Desserts & Bakery", "department": "Bakery", "tax_slab": 0.05}
        ],
        "products": [
            {"sku": "REST-APP-001", "name": "Peri Peri French Fries", "category": "Starters & Appetizers", "cost": 60.00, "price": 140.00, "stock": 150, "reorder": 30, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-APP-002", "name": "Paneer Tikka Charcoal Grilled (6pcs)", "category": "Starters & Appetizers", "cost": 110.00, "price": 240.00, "stock": 70, "reorder": 18, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-APP-003", "name": "Crispy Glazed Chicken Wings (6pcs)", "category": "Starters & Appetizers", "cost": 130.00, "price": 280.00, "stock": 80, "reorder": 20, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-APP-004", "name": "Garlic Breadsticks with Mozzarella", "category": "Starters & Appetizers", "cost": 75.00, "price": 160.00, "stock": 90, "reorder": 20, "lead_time": 1, "shelf_life": 2},

            {"sku": "REST-PIZ-001", "name": "Farmhouse Supreme Pizza (10in)", "category": "Woodfired Pizzas & Pastas", "cost": 145.00, "price": 340.00, "stock": 100, "reorder": 25, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-PIZ-002", "name": "Chicken Pepperoni Pizza (10in)", "category": "Woodfired Pizzas & Pastas", "cost": 180.00, "price": 420.00, "stock": 85, "reorder": 20, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-PIZ-003", "name": "Creamy Alfredo White Sauce Pasta", "category": "Woodfired Pizzas & Pastas", "cost": 110.00, "price": 260.00, "stock": 75, "reorder": 18, "lead_time": 1, "shelf_life": 2},

            {"sku": "REST-MAIN-001", "name": "Butter Chicken Gravy", "category": "Main Course & Curries", "cost": 160.00, "price": 360.00, "stock": 70, "reorder": 18, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-MAIN-002", "name": "Paneer Butter Masala", "category": "Main Course & Curries", "cost": 125.00, "price": 280.00, "stock": 75, "reorder": 18, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-MAIN-003", "name": "Dal Makhani Slow Cooked", "category": "Main Course & Curries", "cost": 95.00, "price": 220.00, "stock": 85, "reorder": 20, "lead_time": 1, "shelf_life": 2},

            {"sku": "REST-BRD-001", "name": "Butter Garlic Naan (2pcs)", "category": "Breads & Rice Combos", "cost": 30.00, "price": 80.00, "stock": 200, "reorder": 40, "lead_time": 1, "shelf_life": 1},
            {"sku": "REST-BRD-002", "name": "Dum Chicken Biryani with Raita", "category": "Breads & Rice Combos", "cost": 140.00, "price": 310.00, "stock": 90, "reorder": 20, "lead_time": 1, "shelf_life": 2},

            {"sku": "REST-BEV-001", "name": "Kulhad Masala Chai", "category": "Beverages & Mocktails", "cost": 15.00, "price": 45.00, "stock": 250, "reorder": 50, "lead_time": 1, "shelf_life": 1},
            {"sku": "REST-BEV-002", "name": "Classic Fresh Mint Mojito", "category": "Beverages & Mocktails", "cost": 45.00, "price": 130.00, "stock": 140, "reorder": 30, "lead_time": 1, "shelf_life": 2},
            {"sku": "REST-BEV-003", "name": "Iced Hazelnut Cold Coffee", "category": "Beverages & Mocktails", "cost": 55.00, "price": 150.00, "stock": 130, "reorder": 25, "lead_time": 1, "shelf_life": 2},

            {"sku": "REST-DES-001", "name": "Sizzling Brownie with Vanilla Ice Cream", "category": "Desserts & Bakery", "cost": 70.00, "price": 180.00, "stock": 60, "reorder": 15, "lead_time": 1, "shelf_life": 3},
            {"sku": "REST-DES-002", "name": "Gulab Jamun with Rabdi (2pcs)", "category": "Desserts & Bakery", "cost": 40.00, "price": 110.00, "stock": 70, "reorder": 18, "lead_time": 1, "shelf_life": 3}
        ],
        "affinity_bundles": [
            ("Butter Chicken Gravy", "Butter Garlic Naan (2pcs)", "Gulab Jamun with Rabdi (2pcs)"),
            ("Farmhouse Supreme Pizza (10in)", "Garlic Breadsticks with Mozzarella", "Classic Fresh Mint Mojito"),
            ("Dum Chicken Biryani with Raita", "Iced Hazelnut Cold Coffee", "Sizzling Brownie with Vanilla Ice Cream"),
            ("Paneer Butter Masala", "Butter Garlic Naan (2pcs)", "Kulhad Masala Chai")
        ]
    },

    "fashion": {
        "domain_key": "fashion",
        "business_name": "VoguePulse Apparel & Couture",
        "tagline": "Modern Indian Wear, Casuals & Formal Attire",
        "currency": "₹",
        "tax_rate": 0.12,
        "categories": [
            {"name": "Men's Casual Wear", "department": "Men", "tax_slab": 0.12},
            {"name": "Men's Formal & Suiting", "department": "Men", "tax_slab": 0.12},
            {"name": "Women's Western & Fusion", "department": "Women", "tax_slab": 0.12},
            {"name": "Women's Ethnic Wear", "department": "Women", "tax_slab": 0.12},
            {"name": "Footwear & Shoes", "department": "Footwear", "tax_slab": 0.12},
            {"name": "Accessories & Leather", "department": "Accessories", "tax_slab": 0.18}
        ],
        "products": [
            {"sku": "FASH-MCAS-001", "name": "Pure Supima Cotton Crew T-Shirt", "category": "Men's Casual Wear", "cost": 290.00, "price": 699.00, "stock": 90, "reorder": 20, "lead_time": 7, "shelf_life": 730},
            {"sku": "FASH-MCAS-002", "name": "Slim Fit Stretch Denim Jeans", "category": "Men's Casual Wear", "cost": 650.00, "price": 1499.00, "stock": 80, "reorder": 18, "lead_time": 10, "shelf_life": 730},
            {"sku": "FASH-MCAS-003", "name": "Vintage Denim Trucker Jacket", "category": "Men's Casual Wear", "cost": 1100.00, "price": 2499.00, "stock": 45, "reorder": 12, "lead_time": 12, "shelf_life": 730},

            {"sku": "FASH-MFOR-001", "name": "Woolen Blend Tailored Formal Blazer", "category": "Men's Formal & Suiting", "cost": 1950.00, "price": 4499.00, "stock": 30, "reorder": 8, "lead_time": 14, "shelf_life": 730},
            {"sku": "FASH-MFOR-002", "name": "Non-Iron Egyptian Cotton Dress Shirt", "category": "Men's Formal & Suiting", "cost": 550.00, "price": 1299.00, "stock": 75, "reorder": 18, "lead_time": 10, "shelf_life": 730},
            {"sku": "FASH-MFOR-003", "name": "Slim Fit Formal Trousers", "category": "Men's Formal & Suiting", "cost": 620.00, "price": 1499.00, "stock": 60, "reorder": 15, "lead_time": 10, "shelf_life": 730},

            {"sku": "FASH-WWES-001", "name": "Floral Tiered Midi Dress", "category": "Women's Western & Fusion", "cost": 720.00, "price": 1699.00, "stock": 65, "reorder": 15, "lead_time": 10, "shelf_life": 540},
            {"sku": "FASH-WWES-002", "name": "High-Waist Wide Leg Denim Jeans", "category": "Women's Western & Fusion", "cost": 780.00, "price": 1899.00, "stock": 70, "reorder": 18, "lead_time": 10, "shelf_life": 730},

            {"sku": "FASH-WETH-001", "name": "Embroidered Silk Anarkali Suit Set", "category": "Women's Ethnic Wear", "cost": 1450.00, "price": 3499.00, "stock": 40, "reorder": 10, "lead_time": 14, "shelf_life": 730},
            {"sku": "FASH-WETH-002", "name": "Pure Cotton Chikankari Kurti", "category": "Women's Ethnic Wear", "cost": 620.00, "price": 1499.00, "stock": 55, "reorder": 12, "lead_time": 12, "shelf_life": 730},

            {"sku": "FASH-FOOT-001", "name": "Classic White Leather Low-Top Sneakers", "category": "Footwear & Shoes", "cost": 820.00, "price": 1899.00, "stock": 60, "reorder": 15, "lead_time": 10, "shelf_life": 730},
            {"sku": "FASH-FOOT-002", "name": "Handcrafted Leather Formal Oxford Shoes", "category": "Footwear & Shoes", "cost": 1350.00, "price": 2999.00, "stock": 35, "reorder": 8, "lead_time": 14, "shelf_life": 730},

            {"sku": "FASH-ACCS-001", "name": "Full Grain Leather Reversible Belt", "category": "Accessories & Leather", "cost": 280.00, "price": 699.00, "stock": 80, "reorder": 18, "lead_time": 7, "shelf_life": 1095},
            {"sku": "FASH-ACCS-002", "name": "Leather Bifold Minimalist Wallet", "category": "Accessories & Leather", "cost": 240.00, "price": 599.00, "stock": 90, "reorder": 20, "lead_time": 6, "shelf_life": 1095},
            {"sku": "FASH-ACCS-003", "name": "Polarized Acetate Sunglasses", "category": "Accessories & Leather", "cost": 520.00, "price": 1299.00, "stock": 50, "reorder": 12, "lead_time": 8, "shelf_life": 1095}
        ],
        "affinity_bundles": [
            ("Pure Supima Cotton Crew T-Shirt", "Slim Fit Stretch Denim Jeans", "Classic White Leather Low-Top Sneakers"),
            ("Woolen Blend Tailored Formal Blazer", "Non-Iron Egyptian Cotton Dress Shirt", "Slim Fit Formal Trousers", "Handcrafted Leather Formal Oxford Shoes"),
            ("Slim Fit Formal Trousers", "Full Grain Leather Reversible Belt", "Leather Bifold Minimalist Wallet")
        ]
    },

    "electronics": {
        "domain_key": "electronics",
        "business_name": "TechPulse Electronics & Gadgets",
        "tagline": "Smartphones, Computing, Audio & Fast Charging",
        "currency": "₹",
        "tax_rate": 0.18,
        "categories": [
            {"name": "Smartphones & Wearables", "department": "Mobile", "tax_slab": 0.18},
            {"name": "Laptops & Computing", "department": "Computers", "tax_slab": 0.18},
            {"name": "Wireless Audio & Sound", "department": "Audio", "tax_slab": 0.18},
            {"name": "Gaming & Peripherals", "department": "Gaming", "tax_slab": 0.18},
            {"name": "Power & Fast Charging", "department": "Accessories", "tax_slab": 0.18}
        ],
        "products": [
            {"sku": "ELEC-MOBL-001", "name": "Apex 5G Flagship Smartphone 256GB", "category": "Smartphones & Wearables", "cost": 32000.00, "price": 44999.00, "stock": 25, "reorder": 6, "lead_time": 4, "shelf_life": 730},
            {"sku": "ELEC-MOBL-002", "name": "Nova 5G Mid-Range Smartphone 128GB", "category": "Smartphones & Wearables", "cost": 13500.00, "price": 18999.00, "stock": 40, "reorder": 10, "lead_time": 4, "shelf_life": 730},
            {"sku": "ELEC-MOBL-003", "name": "Pulse Pro Smartwatch AMOLED", "category": "Smartphones & Wearables", "cost": 1600.00, "price": 2999.00, "stock": 50, "reorder": 12, "lead_time": 5, "shelf_life": 730},

            {"sku": "ELEC-LAPT-001", "name": "Thin & Light Core i5 Laptop (16GB/512GB)", "category": "Laptops & Computing", "cost": 42000.00, "price": 54999.00, "stock": 18, "reorder": 5, "lead_time": 7, "shelf_life": 730},
            {"sku": "ELEC-LAPT-002", "name": "Creator RTX Gaming Laptop (16GB/1TB SSD)", "category": "Laptops & Computing", "cost": 68000.00, "price": 84999.00, "stock": 12, "reorder": 4, "lead_time": 8, "shelf_life": 730},

            {"sku": "ELEC-AUD-001", "name": "Active Noise Cancelling Wireless Headphones", "category": "Wireless Audio & Sound", "cost": 3200.00, "price": 4999.00, "stock": 45, "reorder": 10, "lead_time": 4, "shelf_life": 730},
            {"sku": "ELEC-AUD-002", "name": "True Wireless ANC Earbuds", "category": "Wireless Audio & Sound", "cost": 1450.00, "price": 2299.00, "stock": 70, "reorder": 18, "lead_time": 4, "shelf_life": 730},
            {"sku": "ELEC-AUD-003", "name": "Portable Waterproof Bluetooth Speaker 16W", "category": "Wireless Audio & Sound", "cost": 1150.00, "price": 1899.00, "stock": 55, "reorder": 12, "lead_time": 4, "shelf_life": 730},

            {"sku": "ELEC-GAME-001", "name": "Mechanical RGB Gaming Keyboard (Hot-Swap)", "category": "Gaming & Peripherals", "cost": 1750.00, "price": 2699.00, "stock": 45, "reorder": 10, "lead_time": 5, "shelf_life": 1095},
            {"sku": "ELEC-GAME-002", "name": "Wireless Ergonomic Gaming Mouse", "category": "Gaming & Peripherals", "cost": 950.00, "price": 1499.00, "stock": 60, "reorder": 15, "lead_time": 5, "shelf_life": 1095},

            {"sku": "ELEC-POW-001", "name": "65W GaN Fast Charger 3-Port", "category": "Power & Fast Charging", "cost": 750.00, "price": 1299.00, "stock": 80, "reorder": 20, "lead_time": 4, "shelf_life": 1095},
            {"sku": "ELEC-POW-002", "name": "20,000mAh Fast Charging Power Bank", "category": "Power & Fast Charging", "cost": 1100.00, "price": 1699.00, "stock": 65, "reorder": 15, "lead_time": 4, "shelf_life": 730},
            {"sku": "ELEC-POW-003", "name": "9H Tempered Glass Screen Protector (2pk)", "category": "Power & Fast Charging", "cost": 85.00, "price": 199.00, "stock": 180, "reorder": 40, "lead_time": 3, "shelf_life": 1095}
        ],
        "affinity_bundles": [
            ("Apex 5G Flagship Smartphone 256GB", "9H Tempered Glass Screen Protector (2pk)", "65W GaN Fast Charger 3-Port"),
            ("Nova 5G Mid-Range Smartphone 128GB", "True Wireless ANC Earbuds", "20,000mAh Fast Charging Power Bank"),
            ("Mechanical RGB Gaming Keyboard (Hot-Swap)", "Wireless Ergonomic Gaming Mouse")
        ]
    },

    "ecommerce": {
        "domain_key": "ecommerce",
        "business_name": "OmniCart Direct D2C Marketplace",
        "tagline": "Home, Fitness, Beauty & Lifestyle Delivered Nationwide",
        "currency": "₹",
        "tax_rate": 0.12,
        "categories": [
            {"name": "Home & Kitchen", "department": "Lifestyle", "tax_slab": 0.12},
            {"name": "Fitness & Sports", "department": "Sports", "tax_slab": 0.12},
            {"name": "Beauty & Personal Care", "department": "Cosmetics", "tax_slab": 0.18},
            {"name": "Stationery & Desk", "department": "Office", "tax_slab": 0.12}
        ],
        "products": [
            {"sku": "ECOM-HOME-001", "name": "Digital Air Fryer 6L Rapid Crisp", "category": "Home & Kitchen", "cost": 3100.00, "price": 4999.00, "stock": 35, "reorder": 8, "lead_time": 5, "shelf_life": 1095},
            {"sku": "ECOM-HOME-002", "name": "Cold Brew Coffee Pitcher with Filter", "category": "Home & Kitchen", "cost": 550.00, "price": 899.00, "stock": 60, "reorder": 15, "lead_time": 5, "shelf_life": 1095},
            {"sku": "ECOM-HOME-003", "name": "Chef Stainless Steel Knife Set (3pc)", "category": "Home & Kitchen", "cost": 750.00, "price": 1299.00, "stock": 45, "reorder": 10, "lead_time": 6, "shelf_life": 1095},

            {"sku": "ECOM-FIT-001", "name": "High-Density Anti-Skid Yoga Mat 6mm", "category": "Fitness & Sports", "cost": 480.00, "price": 799.00, "stock": 70, "reorder": 18, "lead_time": 5, "shelf_life": 1095},
            {"sku": "ECOM-FIT-002", "name": "Adjustable Rubber Dumbbells Pair (10kg)", "category": "Fitness & Sports", "cost": 2100.00, "price": 3499.00, "stock": 25, "reorder": 6, "lead_time": 8, "shelf_life": 1825},
            {"sku": "ECOM-FIT-003", "name": "Insulated Stainless Steel Gym Sipper 1L", "category": "Fitness & Sports", "cost": 360.00, "price": 599.00, "stock": 80, "reorder": 20, "lead_time": 4, "shelf_life": 1095},

            {"sku": "ECOM-BEAU-001", "name": "10% Niacinamide Face Glow Serum (30ml)", "category": "Beauty & Personal Care", "cost": 290.00, "price": 549.00, "stock": 90, "reorder": 20, "lead_time": 4, "shelf_life": 730},
            {"sku": "ECOM-BEAU-002", "name": "Hyaluronic Acid Hydrating Gel (100ml)", "category": "Beauty & Personal Care", "cost": 280.00, "price": 499.00, "stock": 75, "reorder": 18, "lead_time": 4, "shelf_life": 730},

            {"sku": "ECOM-BOOK-001", "name": "Hardcover Bullet Journal with Pen", "category": "Stationery & Desk", "cost": 240.00, "price": 449.00, "stock": 85, "reorder": 20, "lead_time": 4, "shelf_life": 1095},
            {"sku": "ECOM-BOOK-002", "name": "Minimalist Acrylic Desk Organizer", "category": "Stationery & Desk", "cost": 210.00, "price": 399.00, "stock": 65, "reorder": 15, "lead_time": 4, "shelf_life": 1095}
        ],
        "affinity_bundles": [
            ("High-Density Anti-Skid Yoga Mat 6mm", "Insulated Stainless Steel Gym Sipper 1L", "Adjustable Rubber Dumbbells Pair (10kg)"),
            ("10% Niacinamide Face Glow Serum (30ml)", "Hyaluronic Acid Hydrating Gel (100ml)"),
            ("Digital Air Fryer 6L Rapid Crisp", "Chef Stainless Steel Knife Set (3pc)")
        ]
    }
}


def get_domain_config(domain_key: str) -> Dict[str, Any]:
    """Retrieves domain specifications by key, falling back to supermarket."""
    return DOMAIN_CATALOGS.get(domain_key.lower(), DOMAIN_CATALOGS["supermarket"])
