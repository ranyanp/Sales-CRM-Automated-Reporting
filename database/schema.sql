
-- ============================================
-- Sales CRM - Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS sales_crm;

USE sales_crm;

-- 1. Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(20),
    address TEXT
);

-- 2. Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    order_status VARCHAR(30),
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

-- 3. Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_price DECIMAL(10,2) NOT NULL
);

-- 4. Order Items table
CREATE TABLE IF NOT EXISTS order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- 5. Report Email Logs table
CREATE TABLE IF NOT EXISTS report_email_logs (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    report_month DATE NOT NULL,
    report_status VARCHAR(20) DEFAULT 'Pending',
    sent_at DATETIME NULL,
    error_message TEXT NULL,
    attempt_count INT DEFAULT 0,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),
    UNIQUE (customer_id, report_month)
);
