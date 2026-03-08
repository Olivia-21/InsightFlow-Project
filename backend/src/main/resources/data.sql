-- =========================================
-- 1. USERS
-- =========================================
CREATE TABLE Users (
    user_id     SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    phone       VARCHAR(20),
    address     TEXT,
    role        VARCHAR(20) DEFAULT 'user',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Users (name, email, password, phone, address, role) VALUES
('Alice Johnson',  'alice@example.com',   'hashed_password_1', '+1-202-555-0101', '123 Maple St, New York, NY',       'admin'),
('Bob Smith',      'bob@example.com',     'hashed_password_2', '+1-202-555-0102', '456 Oak Ave, Los Angeles, CA',     'user'),
('Carol White',    'carol@example.com',   'hashed_password_3', '+1-202-555-0103', '789 Pine Rd, Chicago, IL',         'user'),
('David Brown',    'david@example.com',   'hashed_password_4', '+1-202-555-0104', '321 Elm St, Houston, TX',          'user'),
('Eva Martinez',   'eva@example.com',     'hashed_password_5', '+1-202-555-0105', '654 Cedar Blvd, Phoenix, AZ',      'user'),
('Frank Wilson',   'frank@example.com',   'hashed_password_6', '+1-202-555-0106', '987 Birch Ln, Philadelphia, PA',   'user'),
('Grace Lee',      'grace@example.com',   'hashed_password_7', '+1-202-555-0107', '147 Walnut Dr, San Antonio, TX',   'user'),
('Henry Taylor',   'henry@example.com',   'hashed_password_8', '+1-202-555-0108', '258 Spruce Ct, San Diego, CA',     'user');

-- =========================================
-- 2. STORES
-- =========================================
CREATE TABLE Stores (
    store_id    SERIAL PRIMARY KEY,
    store_name  VARCHAR(150) NOT NULL,
    email       VARCHAR(150),
    phone       VARCHAR(20),
    address     TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Stores (store_name, email, phone, address) VALUES
('Tech World', 'tech@store.com', '+1-555-1001', '12 Silicon Ave, NY'),
('Fashion Hub', 'fashion@store.com', '+1-555-1002', '89 Style St, CA'),
('Home Comforts', 'home@store.com', '+1-555-1003', '45 Living Rd, IL');

-- =========================================
-- 3. CATEGORIES
-- =========================================
CREATE TABLE Categories (
    category_id   SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description   TEXT
);

INSERT INTO Categories (category_name, description) VALUES
('Electronics',     'Devices, gadgets, and accessories'),
('Clothing',        'Men and women apparel and accessories'),
('Home & Kitchen',  'Furniture, cookware, and home essentials'),
('Books',           'Fiction, non-fiction, and educational titles'),
('Sports',          'Equipment and gear for outdoor and indoor sports'),
('Beauty',          'Skincare, haircare, and personal care products');

-- =========================================
-- 4. PRODUCTS
-- =========================================
CREATE TABLE Products (
    product_id   SERIAL PRIMARY KEY,
    name         VARCHAR(150) NOT NULL,
    description  TEXT,
    price        DECIMAL(10,2) NOT NULL,
    category_id  INT,
    store_id     INT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (store_id)    REFERENCES Stores(store_id)
);

INSERT INTO Products (name, description, price, category_id, store_id) VALUES
('Wireless Headphones',      'Noise-cancelling over-ear headphones',           89.99,  1, 1),
('Smartphone 12 Pro',        '6.5-inch OLED display, 128GB storage',          699.99, 1, 1),
('USB-C Hub 7-in-1',         'HDMI, USB 3.0, SD card, and PD charging',       34.99, 1, 1),
('Mens Running Shoes',       'Lightweight mesh shoes for long-distance runs', 59.99, 2, 2),
('Womens Yoga Pants',        'High-waist, four-way stretch fabric',           39.99, 2, 2),
('Denim Jacket',             'Classic blue denim, unisex fit',                49.99, 2, 2),
('Non-stick Cookware Set',   '10-piece set with lids, oven-safe to 400F',    79.99, 3, 3),
('Standing Desk',            'Height-adjustable, 55x28 inch surface',        249.99, 3, 3),
('Cotton Bed Sheets',        'Queen size, 400 thread count, white',          44.99, 3, 3),
('The Pragmatic Programmer', 'Classic software engineering reference',        42.00, 4, 3),
('Atomic Habits',            'Guide to building good habits',                 16.99, 4, 3),
('Yoga Mat',                 'Non-slip, 6mm thick, with carry strap',        25.99, 5, 3),
('Resistance Bands Set',     'Five resistance levels, latex-free',           18.99, 5, 3),
('Vitamin C Serum',          '20% concentration, with hyaluronic acid',      22.99, 6, 3),
('Electric Toothbrush',      'Sonic technology, 3 brushing modes',           49.99, 6, 3);

-- =========================================
-- 5. STORE INVENTORY
-- =========================================
CREATE TABLE StoreInventory (
    store_inventory_id SERIAL PRIMARY KEY,
    store_id           INT,
    product_id         INT,
    quantity_available INT NOT NULL,
    last_updated       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(store_id, product_id),
    FOREIGN KEY (store_id)    REFERENCES Stores(store_id),
    FOREIGN KEY (product_id)  REFERENCES Products(product_id)
);

-- Trigger to auto-update last_updated
CREATE OR REPLACE FUNCTION update_store_inventory_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_store_inventory_last_updated
BEFORE UPDATE ON StoreInventory
FOR EACH ROW
EXECUTE FUNCTION update_store_inventory_last_updated();

-- Inventory data
INSERT INTO StoreInventory (store_id, product_id, quantity_available) VALUES
(1,  1, 120),
(1,  2, 45),
(1,  3, 200),
(2,  4, 80),
(2,  5, 150),
(2,  6, 60),
(3,  7, 90),
(3,  8, 30),
(3,  9, 110),
(3, 10, 75),
(3, 11, 200),
(3, 12, 180),
(3, 13, 220),
(3, 14, 130),
(3, 15, 95);

-- =========================================
-- 6. ORDERS
-- =========================================
CREATE TABLE Orders (
    order_id     SERIAL PRIMARY KEY,
    user_id      INT,
    order_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status       VARCHAR(50),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Orders (user_id, status, total_amount) VALUES
(2, 'delivered',  789.98),
(3, 'shipped',     79.98),
(4, 'processing', 249.99),
(5, 'delivered',   82.98),
(6, 'cancelled',   42.00),
(7, 'delivered',   44.98),
(8, 'shipped',    699.99);

-- =========================================
-- 7. ORDER ITEMS
-- =========================================
CREATE TABLE OrderItems (
    order_item_id SERIAL PRIMARY KEY,
    order_id      INT,
    product_id    INT,
    quantity      INT NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO OrderItems (order_id, product_id, quantity, unit_price) VALUES
(1,  2, 1, 699.99),
(1,  1, 1,  89.99),
(2,  4, 1,  59.99),
(2,  5, 1,  39.99),
(3,  8, 1, 249.99),
(4, 12, 1,  25.99),
(4, 13, 1,  18.99),
(4, 14, 1,  22.99),
(4, 15, 1,  49.99),
(5, 10, 1,  42.00),
(6,  9, 1,  44.99),
(6,  5, 1,  39.99),
(7,  2, 1, 699.99);

-- =========================================
-- 8. FEEDBACK CATEGORIES
-- =========================================
CREATE TABLE FeedbackCategories (
    feedback_category_id SERIAL PRIMARY KEY,
    category_name        VARCHAR(100) NOT NULL,
    description          TEXT
);

INSERT INTO FeedbackCategories (category_name, description) VALUES
('Product Quality', 'Feedback about product performance'),
('Delivery Experience', 'Feedback about shipping and delivery'),
('Packaging', 'Comments about packaging quality'),
('Customer Service', 'Support experience'),
('Value for Money', 'Product worth relative to price');

-- =========================================
-- 9. REVIEWS
-- =========================================
CREATE TABLE Reviews (
    review_id            SERIAL PRIMARY KEY,
    user_id              INT,
    product_id           INT,
    rating               INT CHECK (rating BETWEEN 1 AND 5),
    comment              TEXT,
    feedback_category_id INT,
    review_date          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)              REFERENCES Users(user_id),
    FOREIGN KEY (product_id)           REFERENCES Products(product_id),
    FOREIGN KEY (feedback_category_id) REFERENCES FeedbackCategories(feedback_category_id)
);

INSERT INTO Reviews (user_id, product_id, rating, comment, feedback_category_id) VALUES
(2,  2, 5, 'Excellent phone, very fast and great camera.', 1),
(2,  1, 4, 'Good sound quality, comfortable fit.', 1),
(3,  4, 5, 'Perfect for daily runs, very lightweight.', 1),
(3,  5, 4, 'Great fit and very comfortable.', 1),
(4,  8, 5, 'Sturdy desk, easy to assemble.', 1),
(5, 12, 5, 'Best yoga mat I have owned.', 1),
(5, 13, 4, 'Good resistance levels, durable bands.', 1),
(6, 10, 5, 'A must-read for every developer.', 1),
(7,  9, 4, 'Soft sheets, true to size.', 1),
(8,  2, 5, 'Worth every penny.', 1);

-- =========================================
-- 10. CARTS
-- =========================================
CREATE TABLE Carts (
    cart_id    SERIAL PRIMARY KEY,
    user_id    INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION update_carts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_carts_updated_at
BEFORE UPDATE ON Carts
FOR EACH ROW
EXECUTE FUNCTION update_carts_updated_at();

INSERT INTO Carts (user_id) VALUES (2),(3),(4),(5),(6),(7),(8);

-- =========================================
-- 11. CART ITEMS
-- =========================================
CREATE TABLE CartItems (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id      INT NOT NULL,
    product_id   INT NOT NULL,
    quantity     INT NOT NULL DEFAULT 1,
    added_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id)    REFERENCES Carts(cart_id)        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)  ON DELETE CASCADE,
    CONSTRAINT unique_cart_product UNIQUE (cart_id, product_id)
);

CREATE OR REPLACE FUNCTION update_cartitems_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_cartitems_updated_at
BEFORE UPDATE ON CartItems
FOR EACH ROW
EXECUTE FUNCTION update_cartitems_updated_at();

INSERT INTO CartItems (cart_id, product_id, quantity) VALUES
(1,  3, 1),
(1,  7, 1),
(2,  6, 2),
(2, 11, 1),
(3,  1, 1),
(4, 15, 1),
(4, 14, 2),
(5, 10, 1),
(6, 12, 1),
(6, 13, 1),
(7,  8, 1);