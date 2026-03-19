from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Database connection
import os

conn = psycopg2.connect(
    host="localhost",
    database="wholesale_erp",
    user="postgres",
    password="5588",
    port="5432"
)

# =========================
# DASHBOARD
# =========================
@app.route("/")
def dashboard():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM products LIMIT 100")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM customers LIMIT 100")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders LIMIT 100")
    total_orders = cur.fetchone()[0]

    cur.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_customers=total_customers,
        total_orders=total_orders
    )


# =========================
# PRODUCTS (WITH SEARCH)
# =========================
@app.route("/products", methods=["GET", "POST"])
def products():

    cur = conn.cursor()

    # Add product
    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        cur.execute("""
        INSERT INTO products(name, category, price, stock_quantity)
        VALUES (%s,%s,%s,%s)
        """, (name, category, price, stock))

        conn.commit()

        return redirect("/products")

    # Search feature
    search = request.args.get("search")

    if search:
        cur.execute(
            "SELECT * FROM products WHERE name ILIKE %s",
            ('%' + search + '%',)
        )
    else:
        cur.execute("SELECT * FROM products")

    product_list = cur.fetchall()

    cur.close()

    return render_template(
        "products.html",
        products=product_list
    )


# DELETE PRODUCT
@app.route("/delete_product/<int:id>")
def delete_product(id):

    cur = conn.cursor()

    cur.execute("DELETE FROM order_items WHERE product_id=%s", (id,))
    cur.execute("DELETE FROM products WHERE product_id=%s", (id,))

    conn.commit()
    cur.close()

    return redirect("/products")


# =========================
# CUSTOMERS
# =========================
@app.route("/customers", methods=["GET", "POST"])
def customers():

    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        contact = request.form["contact"]
        address = request.form["address"]

        cur.execute("""
        INSERT INTO customers(name, contact, address)
        VALUES (%s,%s,%s)
        """, (name, contact, address))

        conn.commit()

        return redirect("/customers")

    cur.execute("SELECT * FROM customers")
    customer_list = cur.fetchall()

    cur.close()

    return render_template("customers.html", customers=customer_list)


# DELETE CUSTOMER
@app.route("/delete_customer/<int:id>")
def delete_customer(id):

    cur = conn.cursor()

    cur.execute("""
        DELETE FROM order_items
        WHERE order_id IN (
            SELECT order_id FROM orders WHERE customer_id=%s
        )
    """, (id,))

    cur.execute("DELETE FROM orders WHERE customer_id=%s", (id,))
    cur.execute("DELETE FROM customers WHERE customer_id=%s", (id,))

    conn.commit()
    cur.close()

    return redirect("/customers")


# =========================
# ORDERS
# =========================
@app.route("/orders", methods=["GET", "POST"])
def orders():

    cur = conn.cursor()

    if request.method == "POST":

        customer_id = request.form["customer"]
        product_id = request.form["product"]
        quantity = int(request.form["quantity"])

        cur.execute("SELECT price FROM products WHERE product_id=%s", (product_id,))
        price = cur.fetchone()[0]

        total = price * quantity

        cur.execute("""
        INSERT INTO orders(customer_id, order_date, total_amount)
        VALUES (%s, NOW(), %s)
        RETURNING order_id
        """, (customer_id, total))

        order_id = cur.fetchone()[0]

        cur.execute("""
        INSERT INTO order_items(order_id, product_id, quantity, price)
        VALUES (%s,%s,%s,%s)
        """, (order_id, product_id, quantity, price))

        cur.execute("""
        UPDATE products
        SET stock_quantity = stock_quantity - %s
        WHERE product_id=%s
        """, (quantity, product_id))

        conn.commit()

        return redirect("/orders")

    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    cur.execute("SELECT * FROM orders")
    order_list = cur.fetchall()

    cur.close()

    return render_template(
        "orders.html",
        customers=customers,
        products=products,
        orders=order_list
    )


# DELETE ORDER
@app.route("/delete_order/<int:id>")
def delete_order(id):

    cur = conn.cursor()

    cur.execute("DELETE FROM order_items WHERE order_id=%s", (id,))
    cur.execute("DELETE FROM orders WHERE order_id=%s", (id,))

    conn.commit()
    cur.close()

    return redirect("/orders")


# =========================
# SALES ANALYSIS
# =========================
@app.route("/sales")
def sales():

    cur = conn.cursor()

    cur.execute("""
    SELECT p.name, SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.name
    ORDER BY total_sold DESC
    """)

    top_products = cur.fetchall()

    cur.execute("""
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(total_amount)
    FROM orders
    GROUP BY month
    ORDER BY month
    """)

    monthly_sales = cur.fetchall()

    cur.close()

    return render_template(
        "analysis.html",
        top_products=top_products,
        monthly_sales=monthly_sales
    )


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
