-- =========================
-- CREATE TABLES
-- =========================

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock_quantity INT
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    address VARCHAR(200)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    price DECIMAL(10,2)
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    product_supplied VARCHAR(100)
);

-- =========================
-- SAMPLE DATA
-- =========================

INSERT INTO products(name, category, price, stock_quantity)
VALUES ('Rice', 'Grains', 40, 1000);

INSERT INTO customers(name, contact, address)
VALUES ('ABC Retailers', '9876543210', 'Main Bazar');

INSERT INTO suppliers(name, contact, product_supplied)
VALUES ('XYZ Traders', '9123456780', 'Rice');

INSERT INTO orders(customer_id, order_date, total_amount)
VALUES (1, '2025-04-07', 4000);

INSERT INTO order_items(order_id, product_id, quantity, price)
VALUES (1, 1, 100, 40);

-- =========================
-- BASIC QUERIES
-- =========================

SELECT * FROM products;
SELECT * FROM customers;
SELECT * FROM orders;

-- =========================
-- JOIN QUERIES
-- =========================

-- Order details with customer & product
SELECT o.order_id, c.name AS customer, p.name AS product, oi.quantity, oi.price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- Supplier-wise product list
SELECT s.name AS supplier, s.product_supplied
FROM suppliers s;

-- Monthly sales report
SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(total_amount) AS total_sales
FROM orders
GROUP BY month
ORDER BY month;

-- =========================
-- NESTED QUERIES
-- =========================

-- Top 5 customers by order value
SELECT name FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    ORDER BY SUM(total_amount) DESC
    LIMIT 5
);

-- Products with low stock
SELECT * FROM products
WHERE stock_quantity < 50;

-- Orders above average value
SELECT * FROM orders
WHERE total_amount > (
    SELECT AVG(total_amount) FROM orders
);

-- =========================
-- FUNCTION
-- =========================

-- Total stock value
CREATE OR REPLACE FUNCTION total_stock_value()
RETURNS DECIMAL AS $$
DECLARE total DECIMAL;
BEGIN
    SELECT SUM(price * stock_quantity) INTO total FROM products;
    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Top selling products
CREATE OR REPLACE FUNCTION top_selling_products()
RETURNS TABLE(product_name VARCHAR, total_sold INT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, SUM(oi.quantity)
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.name
    ORDER BY SUM(oi.quantity) DESC;
END;
$$ LANGUAGE plpgsql;

-- =========================
-- PROCEDURE
-- =========================

CREATE OR REPLACE PROCEDURE place_order(
    c_id INT,
    p_id INT,
    qty INT
)
LANGUAGE plpgsql
AS $$
DECLARE price_val DECIMAL;
DECLARE new_order INT;
BEGIN
    SELECT price INTO price_val FROM products WHERE product_id = p_id;

    INSERT INTO orders(customer_id, order_date, total_amount)
    VALUES (c_id, CURRENT_DATE, price_val * qty)
    RETURNING order_id INTO new_order;

    INSERT INTO order_items(order_id, product_id, quantity, price)
    VALUES (new_order, p_id, qty, price_val);

    UPDATE products
    SET stock_quantity = stock_quantity - qty
    WHERE product_id = p_id;
END;
$$;

-- =========================
-- VIEWS
-- =========================

-- Customer order summary
CREATE VIEW customer_order_summary AS
SELECT c.name, COUNT(o.order_id) AS total_orders, SUM(o.total_amount) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;

-- Product-wise sales
CREATE VIEW product_sales AS
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.name;

-- Supplier-product mapping
CREATE VIEW supplier_products AS
SELECT name, product_supplied
FROM suppliers;