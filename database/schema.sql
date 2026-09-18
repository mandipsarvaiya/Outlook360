-- ====================================================================
-- OmniPulse AI - Universal Enterprise Relational Database Schema
-- Compatible with MySQL 8.0+ and SQLite (ANSI SQL Compliant)
-- Designed in 3NF Normal Form with Foreign Key Integrity & Indexing
-- ====================================================================

-- 1. System Users & Role-Based Access Control (RBAC)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    role VARCHAR(30) NOT NULL, -- 'owner', 'cashier', 'inventory_staff'
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Business Profile & Active Domain Metadata
CREATE TABLE IF NOT EXISTS business_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_key VARCHAR(50) NOT NULL,
    business_name VARCHAR(150) NOT NULL,
    currency VARCHAR(10) DEFAULT '₹',
    tax_rate DECIMAL(5,2) DEFAULT 0.05,
    tagline VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    description TEXT,
    tax_slab_percent DECIMAL(5,2) DEFAULT 0.00
);

-- 4. Products Catalog (Universal SKU / Service Catalog)
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    category_id INTEGER NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    current_stock INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 15,
    lead_time_days INTEGER NOT NULL DEFAULT 3,
    shelf_life_days INTEGER DEFAULT 365,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- 5. Customers Table (Demographics & Profiles)
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120),
    phone VARCHAR(30),
    gender VARCHAR(20),
    age_group VARCHAR(30),
    city VARCHAR(80),
    tier VARCHAR(30) DEFAULT 'Standard',
    registered_at DATE NOT NULL
);

-- 6. Orders Table (Header Invoices)
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no VARCHAR(50) UNIQUE NOT NULL,
    order_date DATETIME NOT NULL,
    customer_id INTEGER NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    channel VARCHAR(50) DEFAULT 'In-Store',
    subtotal DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'Completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- 7. Order Items Table (Line Items)
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    profit_margin DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);

-- 8. Inventory Logs (Stock In/Out Ledger)
CREATE TABLE IF NOT EXISTS inventory_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    change_type VARCHAR(50) NOT NULL, -- 'Purchase', 'Sale', 'Return', 'Wastage', 'Adjustment'
    quantity INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    reason VARCHAR(255),
    cost_impact DECIMAL(12,2) DEFAULT 0.00,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);

-- ====================================================================
-- Performance Indexing for High-Speed Analytical Queries
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_users_emp ON users(emp_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_logs_product ON inventory_logs(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_logs_timestamp ON inventory_logs(timestamp);
