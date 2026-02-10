import sqlite3
import json

def init_database():
    """Initialize the SQLite database with mock fast food data"""
    conn = sqlite3.connect('amiHungry.db')
    cursor = conn.cursor()

    # Create restaurants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            cuisine_type TEXT,
            rating REAL,
            delivery_time_min INTEGER,
            delivery_time_max INTEGER,
            delivery_fee REAL,
            minimum_order REAL
        )
    ''')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price REAL NOT NULL,
            calories INTEGER,
            has_offer BOOLEAN DEFAULT 0,
            offer_price REAL,
            offer_description TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')

    # Insert mock restaurants (Greek fast food chains)
    restaurants_data = [
        ('Goody\'s Burger House', 'efood', 'Burgers', 4.5, 20, 30, 1.50, 8.00),
        ('Goody\'s Burger House', 'wolt', 'Burgers', 4.5, 25, 35, 1.90, 10.00),
        ('Everest', 'efood', 'Sandwiches', 4.3, 15, 25, 1.20, 6.00),
        ('Everest', 'wolt', 'Sandwiches', 4.3, 18, 28, 1.50, 7.00),
        ('Pizza Fan', 'efood', 'Pizza', 4.4, 30, 45, 2.00, 12.00),
        ('Pizza Fan', 'wolt', 'Pizza', 4.4, 28, 40, 1.80, 10.00),
        ('KFC', 'efood', 'Chicken', 4.2, 25, 35, 1.80, 9.00),
        ('KFC', 'wolt', 'Chicken', 4.2, 22, 32, 2.00, 8.50),
        ('McDonald\'s', 'efood', 'Burgers', 4.1, 20, 30, 1.50, 7.00),
        ('McDonald\'s', 'wolt', 'Burgers', 4.1, 18, 28, 1.70, 6.50),
        ('Subway', 'efood', 'Sandwiches', 4.0, 20, 30, 1.30, 7.50),
        ('Subway', 'wolt', 'Sandwiches', 4.0, 25, 35, 1.60, 8.00),
    ]

    cursor.executemany('''
        INSERT INTO restaurants (name, platform, cuisine_type, rating,
                                delivery_time_min, delivery_time_max, delivery_fee, minimum_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', restaurants_data)

    # Insert mock products
    products_data = [
        # Goody's efood (id=1)
        (1, 'Big Goody\'s', 'Μπιφτέκι μοσχαρίσιο, τυρί cheddar, μπέικον, σάλτσα', 'Burgers', 7.50, 650, 0, None, None),
        (1, 'Chicken Burger', 'Κοτόπουλο πανέ, μαρούλι, τομάτα, μαγιονέζα', 'Burgers', 6.80, 520, 1, 5.90, 'Προσφορά -15%'),
        (1, 'Caesar Salad', 'Μαρούλι, κοτόπουλο, παρμεζάνα, croutons', 'Salads', 6.50, 380, 0, None, None),
        (1, 'Πατάτες Τηγανητές', 'Τηγανητές πατάτες μεγάλες', 'Sides', 3.20, 420, 0, None, None),

        # Goody's wolt (id=2)
        (2, 'Big Goody\'s', 'Μπιφτέκι μοσχαρίσιο, τυρί cheddar, μπέικον, σάλτσα', 'Burgers', 7.80, 650, 0, None, None),
        (2, 'Chicken Burger', 'Κοτόπουλο πανέ, μαρούλι, τομάτα, μαγιονέζα', 'Burgers', 7.00, 520, 0, None, None),
        (2, 'Caesar Salad', 'Μαρούλι, κοτόπουλο, παρμεζάνα, croutons', 'Salads', 6.70, 380, 1, 5.90, 'Meal Deal'),
        (2, 'Πατάτες Τηγανητές', 'Τηγανητές πατάτες μεγάλες', 'Sides', 3.50, 420, 0, None, None),

        # Everest efood (id=3)
        (3, 'Club Sandwich', 'Κοτόπουλο, μπέικον, τυρί, μαρούλι, τομάτα', 'Sandwiches', 5.50, 480, 0, None, None),
        (3, 'Τοστ deluxe', 'Ζαμπόν, τυρί, τομάτα', 'Sandwiches', 3.80, 350, 1, 3.20, 'Προσφορά Ημέρας'),
        (3, 'Τυρόπιτα', 'Φρέσκια τυρόπιτα με φύλλο', 'Pastries', 2.50, 280, 0, None, None),
        (3, 'Καφές Φίλτρου', 'Φρεσκοκομμένος καφές', 'Beverages', 2.00, 5, 0, None, None),

        # Everest wolt (id=4)
        (4, 'Club Sandwich', 'Κοτόπουλο, μπέικον, τυρί, μαρούλι, τομάτα', 'Sandwiches', 5.70, 480, 0, None, None),
        (4, 'Τοστ deluxe', 'Ζαμπόν, τυρί, τομάτα', 'Sandwiches', 3.90, 350, 0, None, None),
        (4, 'Τυρόπιτα', 'Φρέσκια τυρόπιτα με φύλλο', 'Pastries', 2.60, 280, 1, 2.20, 'Bundle Offer'),
        (4, 'Καφές Φίλτρου', 'Φρεσκοκομμένος καφές', 'Beverages', 2.10, 5, 0, None, None),

        # Pizza Fan efood (id=5)
        (5, 'Margherita Large', 'Τοματοσάλτσα, μοτσαρέλα, ρίγανη', 'Pizza', 8.90, 920, 0, None, None),
        (5, 'Pepperoni Large', 'Τοματοσάλτσα, μοτσαρέλα, πεπερόνι', 'Pizza', 10.50, 1050, 1, 9.00, '2η Πίτσα -50%'),
        (5, 'Chicken BBQ Large', 'BBQ σάλτσα, κοτόπουλο, κρεμμύδι, μοτσαρέλα', 'Pizza', 11.20, 1100, 0, None, None),
        (5, 'Crazy Bread', 'Ψωμάκια με σκόρδο και τυρί', 'Sides', 4.50, 380, 0, None, None),

        # Pizza Fan wolt (id=6)
        (6, 'Margherita Large', 'Τοματοσάλτσα, μοτσαρέλα, ρίγανη', 'Pizza', 9.20, 920, 0, None, None),
        (6, 'Pepperoni Large', 'Τοματοσάλτσα, μοτσαρέλα, πεπερόνι', 'Pizza', 10.80, 1050, 0, None, None),
        (6, 'Chicken BBQ Large', 'BBQ σάλτσα, κοτόπουλο, κρεμμύδι, μοτσαρέλα', 'Pizza', 11.50, 1100, 1, 10.20, 'Premium Deal'),
        (6, 'Crazy Bread', 'Ψωμάκια με σκόρδο και τυρί', 'Sides', 4.80, 380, 0, None, None),

        # KFC efood (id=7)
        (7, 'Bucket 10 Κομμάτια', '10 κομμάτια τραγανό κοτόπουλο', 'Chicken', 15.90, 2200, 0, None, None),
        (7, 'Zinger Burger', 'Φιλέτο κοτόπουλο crunchy, μαρούλι, μαγιονέζα', 'Burgers', 6.50, 580, 1, 5.50, 'Combo -15%'),
        (7, 'Hot Wings 6τμχ', 'Καυτερές φτερούγες κοτόπουλο', 'Chicken', 5.20, 420, 0, None, None),
        (7, 'Coleslaw', 'Σαλάτα λάχανο', 'Sides', 2.80, 180, 0, None, None),

        # KFC wolt (id=8)
        (8, 'Bucket 10 Κομμάτια', '10 κομμάτια τραγανό κοτόπουλο', 'Chicken', 16.20, 2200, 1, 14.50, 'Family Meal'),
        (8, 'Zinger Burger', 'Φιλέτο κοτόπουλο crunchy, μαρούλι, μαγιονέζα', 'Burgers', 6.70, 580, 0, None, None),
        (8, 'Hot Wings 6τμχ', 'Καυτερές φτερούγες κοτόπουλο', 'Chicken', 5.40, 420, 0, None, None),
        (8, 'Coleslaw', 'Σαλάτα λάχανο', 'Sides', 2.90, 180, 0, None, None),

        # McDonald's efood (id=9)
        (9, 'Big Mac', 'Διπλό μπιφτέκι, ειδική σάλτσα, μαρούλι, τυρί', 'Burgers', 5.50, 540, 0, None, None),
        (9, 'McChicken', 'Κοτόπουλο πανέ, μαγιονέζα, μαρούλι', 'Burgers', 4.80, 490, 1, 4.00, 'Happy Price'),
        (9, 'McNuggets 9τμχ', 'Nuggets κοτόπουλο', 'Chicken', 5.20, 450, 0, None, None),
        (9, 'McFlurry Oreo', 'Παγωτό με Oreo', 'Desserts', 3.50, 380, 0, None, None),

        # McDonald's wolt (id=10)
        (10, 'Big Mac', 'Διπλό μπιφτέκι, ειδική σάλτσα, μαρούλι, τυρί', 'Burgers', 5.70, 540, 1, 4.90, 'Bundle Save'),
        (10, 'McChicken', 'Κοτόπουλο πανέ, μαγιονέζα, μαρούλι', 'Burgers', 5.00, 490, 0, None, None),
        (10, 'McNuggets 9τμχ', 'Nuggets κοτόπουλο', 'Chicken', 5.40, 450, 0, None, None),
        (10, 'McFlurry Oreo', 'Παγωτό με Oreo', 'Desserts', 3.70, 380, 0, None, None),

        # Subway efood (id=11)
        (11, 'Italian B.M.T. 30cm', 'Σαλάμι, πεπερόνι, ζαμπόν, λαχανικά', 'Sandwiches', 7.50, 480, 0, None, None),
        (11, 'Chicken Teriyaki 30cm', 'Κοτόπουλο teriyaki, λαχανικά', 'Sandwiches', 7.80, 520, 1, 6.90, 'Sub of the Day'),
        (11, 'Veggie Delite 15cm', 'Λαχανικά, τυρί', 'Sandwiches', 4.20, 280, 0, None, None),
        (11, 'Cookies 3τμχ', 'Μπισκότα σοκολάτας', 'Desserts', 2.50, 450, 0, None, None),

        # Subway wolt (id=12)
        (12, 'Italian B.M.T. 30cm', 'Σαλάμι, πεπερόνι, ζαμπόν, λαχανικά', 'Sandwiches', 7.80, 480, 0, None, None),
        (12, 'Chicken Teriyaki 30cm', 'Κοτόπουλο teriyaki, λαχανικά', 'Sandwiches', 8.00, 520, 0, None, None),
        (12, 'Veggie Delite 15cm', 'Λαχανικά, τυρί', 'Sandwiches', 4.50, 280, 1, 3.90, 'Healthy Choice'),
        (12, 'Cookies 3τμχ', 'Μπισκότα σοκολάτας', 'Desserts', 2.70, 450, 0, None, None),
    ]

    cursor.executemany('''
        INSERT INTO products (restaurant_id, name, description, category, price, calories,
                            has_offer, offer_price, offer_description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products_data)

    conn.commit()
    conn.close()

    print("Database initialized successfully with mock data!")

def get_all_restaurants():
    """Get all restaurants from database"""
    conn = sqlite3.connect('amiHungry.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM restaurants')
    restaurants = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return restaurants

def get_all_products():
    """Get all products with restaurant info"""
    conn = sqlite3.connect('amiHungry.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, r.name as restaurant_name, r.platform, r.cuisine_type,
               r.rating, r.delivery_time_min, r.delivery_time_max,
               r.delivery_fee, r.minimum_order
        FROM products p
        JOIN restaurants r ON p.restaurant_id = r.id
    ''')
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

def search_products(query=None, category=None, max_price=None, platform=None):
    """Search products with filters"""
    conn = sqlite3.connect('amiHungry.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT p.*, r.name as restaurant_name, r.platform, r.cuisine_type,
               r.rating, r.delivery_time_min, r.delivery_time_max,
               r.delivery_fee, r.minimum_order
        FROM products p
        JOIN restaurants r ON p.restaurant_id = r.id
        WHERE 1=1
    '''
    params = []

    if query:
        sql += ' AND (p.name LIKE ? OR p.description LIKE ?)'
        params.extend([f'%{query}%', f'%{query}%'])

    if category:
        sql += ' AND p.category = ?'
        params.append(category)

    if max_price:
        sql += ' AND p.price <= ?'
        params.append(max_price)

    if platform:
        sql += ' AND r.platform = ?'
        params.append(platform)

    cursor.execute(sql, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

if __name__ == '__main__':
    init_database()
