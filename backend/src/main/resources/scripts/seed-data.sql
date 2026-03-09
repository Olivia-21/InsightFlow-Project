-- Seed data for InsightFlow
-- This script runs AFTER Hibernate creates the schema

-- 1. USERS
INSERT INTO Users (name, email, password, phone, address, role, created_at) VALUES
('Alice Johnson',  'alice@example.com',   'hashed_password_1', '+1-202-555-0101', '123 Maple St, New York, NY',       'admin', CURRENT_TIMESTAMP),
('Bob Smith',      'bob@example.com',     'hashed_password_2', '+1-202-555-0102', '456 Oak Avenue, Los Angeles, CA',  'user',  CURRENT_TIMESTAMP),
('Carol White',    'carol@example.com',   'hashed_password_3', '+1-202-555-0103', '789 Pine Rd, Chicago, IL',         'user',  CURRENT_TIMESTAMP),
('David Brown',    'david@example.com',   'hashed_password_4', '+1-202-555-0104', '321 Elm St, Houston, TX',          'user',  CURRENT_TIMESTAMP),
('Eva Martinez',   'eva@example.com',     'hashed_password_5', '+1-202-555-0105', '654 Cedar Blvd, Phoenix, AZ',      'user',  CURRENT_TIMESTAMP),
('Frank Wilson',   'frank@example.com',   'hashed_password_6', '+1-202-555-0106', '987 Birch Ln, Philadelphia, PA',   'user',  CURRENT_TIMESTAMP),
('Grace Lee',      'grace@example.com',   'hashed_password_7', '+1-202-555-0107', '147 Walnut Dr, San Antonio, TX',   'user',  CURRENT_TIMESTAMP),
('Henry Taylor',   'henry@example.com',   'hashed_password_8', '+1-202-555-0108', '258 Spruce Ct, San Diego, CA',     'user',  CURRENT_TIMESTAMP);

-- 2. STORES
INSERT INTO Stores (store_name, email, phone, region, location, created_at) VALUES
('Tech World', 'tech@store.com', '+1-555-1001', 'North America', '12 Silicon Ave, NY', CURRENT_TIMESTAMP),
('Fashion Hub', 'fashion@store.com', '+1-555-1002', 'Europe', '89 Style St, CA', CURRENT_TIMESTAMP),
('Home Comforts', 'home@store.com', '+1-555-1003', 'Africa', '45 Living Rd, IL', CURRENT_TIMESTAMP);

-- 3. CATEGORIES
INSERT INTO Categories (category_name, description) VALUES
('Electronics',     'Devices, gadgets, and accessories'),
('Clothing',        'Men and women apparel and accessories'),
('Home & Kitchen',  'Furniture, cookware, and home essentials'),
('Books',           'Fiction, non-fiction, and educational titles'),
('Sports',          'Equipment and gear for outdoor and indoor sports'),
('Beauty',          'Skincare, haircare, and personal care products');

-- 4. PRODUCTS
INSERT INTO Products (product_name, description, unit_price, reorder_level, is_active, supplier, category_id, store_id, created_at) VALUES
('Wireless Headphones',      'Noise-cancelling over-ear headphones',           89.99,  10, true,  'Sony',        1, 1, CURRENT_TIMESTAMP),
('Smartphone 12 Pro',        '6.5-inch OLED display, 128GB storage',          699.99,  5,  true,  'Apple',       1, 1, CURRENT_TIMESTAMP),
('USB-C Hub 7-in-1',         'HDMI, USB 3.0, SD card, and PD charging',       34.99,  20, true,  'Anker',       1, 1, CURRENT_TIMESTAMP),
('Mens Running Shoes',       'Lightweight mesh shoes for long-distance runs', 59.99,  15, true,  'Nike',        2, 2, CURRENT_TIMESTAMP),
('Womens Yoga Pants',        'High-waist, four-way stretch fabric',           39.99,  25, true,  'Lululemon',   2, 2, CURRENT_TIMESTAMP),
('Denim Jacket',             'Classic blue denim, unisex fit',                49.99,  10, true,  'Levis',       2, 2, CURRENT_TIMESTAMP),
('Non-stick Cookware Set',   '10-piece set with lids, oven-safe to 400F',    79.99,  8,  true,  'T-fal',       3, 3, CURRENT_TIMESTAMP),
('Standing Desk',            'Height-adjustable, 55x28 inch surface',        249.99,  3,  true,  'Flexispot',   3, 3, CURRENT_TIMESTAMP),
('Cotton Bed Sheets',        'Queen size, 400 thread count, white',          44.99,  12, true,  'Brooklinen',  3, 3, CURRENT_TIMESTAMP),
('The Pragmatic Programmer', 'Classic software engineering reference',        42.00,  10, true,  'Addison',     4, 3, CURRENT_TIMESTAMP),
('Atomic Habits',            'Guide to building good habits',                 16.99,  50, true,  'Penguin',     4, 3, CURRENT_TIMESTAMP),
('Yoga Mat',                 'Non-slip, 6mm thick, with carry strap',        25.99,  30, true,  'Gaiam',       5, 3, CURRENT_TIMESTAMP),
('Resistance Bands Set',     'Five resistance levels, latex-free',           18.99,  40, true,  'FitSimplify', 5, 3, CURRENT_TIMESTAMP),
('Vitamin C Serum',          '20% concentration, with hyaluronic acid',      22.99,  15, true,  'The Ordinary', 6, 3, CURRENT_TIMESTAMP),
('Electric Toothbrush',      'Sonic technology, 3 brushing modes',           49.99,  20, true,  'Oral-B',      6, 3, CURRENT_TIMESTAMP);

-- 5. STORE INVENTORY
INSERT INTO StoreInventory (store_id, product_id, opening_stock, closing_stock, unit_received, unit_sold, needs_reorder, stock_date) VALUES
(1,  1, 150, 120, 20, 50, false, CURRENT_DATE),
(1,  2, 60,  45,  10, 25, false, CURRENT_DATE),
(1,  3, 250, 200, 30, 80, false, CURRENT_DATE),
(2,  4, 100, 80,  20, 40, false, CURRENT_DATE),
(2,  5, 200, 150, 50, 100, false, CURRENT_DATE),
(2,  6, 80,  60,  15, 35, false, CURRENT_DATE),
(3,  7, 120, 90,  25, 55, false, CURRENT_DATE),
(3,  8, 40,  30,  5,  15, false, CURRENT_DATE),
(3,  9, 150, 110, 30, 70, false, CURRENT_DATE),
(3, 10, 100, 75,  20, 45, false, CURRENT_DATE),
(3, 11, 250, 200, 40, 90, false, CURRENT_DATE),
(3, 12, 220, 180, 50, 90, false, CURRENT_DATE),
(3, 13, 300, 220, 60, 140, false, CURRENT_DATE),
(3, 14, 180, 130, 40, 90, false, CURRENT_DATE),
(3, 15, 130, 95,  30, 65, false, CURRENT_DATE);

-- 6. ORDERS
INSERT INTO Orders (user_id, status, total_amount, discount_applied, tax_amount, payment_method, order_date) VALUES
(2, 'delivered',  789.98,  10.00, 60.00, 'Credit Card', CURRENT_DATE),
(3, 'shipped',     79.98,   0.00,  5.00, 'PayPal',      CURRENT_DATE),
(4, 'processing', 249.99,   5.00, 20.00, 'Bank Transfer', CURRENT_DATE),
(5, 'delivered',   82.98,   2.00,  6.50, 'Credit Card', CURRENT_DATE),
(6, 'cancelled',   42.00,   0.00,  3.50, 'Mobile Money', CURRENT_DATE),
(7, 'delivered',   44.98,   0.00,  3.50, 'Cash',        CURRENT_DATE),
(8, 'shipped',    699.99,  50.00, 55.00, 'Credit Card', CURRENT_DATE);

-- 7. ORDER ITEMS
INSERT INTO OrderItems (order_id, product_id, quantity, unit_price, discount_applied, tax_amount) VALUES
(1,  2, 1, 699.99, 40.00, 45.00),
(1,  1, 1,  89.99, 10.00,  5.00),
(2,  4, 1,  59.99,  5.00,  4.00),
(2,  5, 1,  39.99,  0.00,  3.00),
(3,  8, 1, 249.99, 10.00, 15.00),
(4, 12, 1,  25.99,  2.00,  2.00),
(4, 13, 1,  18.99,  1.00,  1.50),
(4, 14, 1,  22.99,  1.00,  1.50),
(4, 15, 1,  49.99,  5.00,  4.00),
(5, 10, 1,  42.00,  2.00,  3.00),
(6,  9, 1,  44.99,  0.00,  3.50),
(6,  5, 1,  39.99,  0.00,  3.00),
(7,  2, 1, 699.99, 50.00, 55.00);

-- 8. FEEDBACK CATEGORIES
INSERT INTO FeedbackCategories (category_name, description) VALUES
('Product Quality', 'Feedback about product performance'),
('Delivery Experience', 'Feedback about shipping and delivery'),
('Packaging', 'Comments about packaging quality'),
('Customer Service', 'Support experience'),
('Value for Money', 'Product worth relative to price');

-- 9. REVIEWS
INSERT INTO Reviews (user_id, product_id, rating, review_text, feedback_category_id, review_date) VALUES
(2,  2, 5, 'Excellent phone, very fast and great camera.', 1, CURRENT_DATE),
(2,  1, 4, 'Good sound quality, comfortable fit.', 1, CURRENT_DATE),
(3,  4, 5, 'Perfect for daily runs, very lightweight.', 1, CURRENT_DATE),
(3,  5, 4, 'Great fit and very comfortable.', 1, CURRENT_DATE),
(4,  8, 5, 'Sturdy desk, easy to assemble.', 1, CURRENT_DATE),
(5, 12, 5, 'Best yoga mat I have owned.', 1, CURRENT_DATE),
(5, 13, 4, 'Good resistance levels, durable bands.', 1, CURRENT_DATE),
(6, 10, 5, 'A must-read for every developer.', 1, CURRENT_DATE),
(7,  9, 4, 'Soft sheets, true to size.', 1, CURRENT_DATE),
(8,  2, 5, 'Worth every penny.', 1, CURRENT_DATE);

-- 10. CARTS
INSERT INTO Carts (user_id, created_at, updated_at) VALUES 
(2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 11. CART ITEMS
INSERT INTO CartItems (cart_id, product_id, quantity, added_at, updated_at) VALUES
(1,  3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1,  7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2,  6, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 11, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3,  1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 15, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 14, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 10, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 12, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 13, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7,  8, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
