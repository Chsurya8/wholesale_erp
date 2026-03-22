from flask import Flask, render_template, request, redirect
import psycopg2
import json

app = Flask(__name__)

# ✅ DB connection
def get_conn():
    return psycopg2.connect(
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

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_customers=total_customers,
        total_orders=total_orders
    )

# =========================
# PRODUCTS
# =========================
@app.route("/products", methods=["GET", "POST"])
def products():

    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO products(name, category, price, stock_quantity)
            VALUES (%s,%s,%s,%s)
        """, (
            request.form["name"],
            request.form["category"],
            request.form["price"],
            request.form["stock"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/products")

    search = request.args.get("search")

    if search:
        cur.execute(
            "SELECT * FROM products WHERE name ILIKE %s",
            ('%' + search + '%',)
        )
    else:
        cur.execute("SELECT * FROM products LIMIT 100")

    product_list = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("products.html", products=product_list)

# =========================
# CUSTOMERS
# =========================
@app.route("/customers", methods=["GET", "POST"])
def customers():

    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            INSERT INTO customers(name, contact, address)
            VALUES (%s,%s,%s)
        """, (
            request.form["name"],
            request.form["contact"],
            request.form["address"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/customers")

    cur.execute("SELECT * FROM customers LIMIT 100")
    customer_list = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("customers.html", customers=customer_list)

# =========================
# ORDERS
# =========================
@app.route("/orders", methods=["GET", "POST"])
def orders():

    conn = get_conn()
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

        cur.close()
        conn.close()

        return redirect("/orders")

    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    cur.execute("SELECT * FROM products LIMIT 100")
    products = cur.fetchall()

    cur.execute("SELECT * FROM orders ORDER BY order_id DESC LIMIT 100")
    order_list = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "orders.html",
        customers=customers,
        products=products,
        orders=order_list
    )

# =========================
# SALES ANALYSIS
# =========================
@app.route("/sales")
def sales():

    conn = get_conn()
    cur = conn.cursor()

    # 🔹 Top products
    cur.execute("""
        SELECT p.name, SUM(oi.quantity)
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.name
        ORDER BY SUM(oi.quantity) DESC
        LIMIT 10
    """)
    top_products = cur.fetchall()

    # 🔹 Monthly sales
    cur.execute("""
        SELECT TO_CHAR(order_date, 'YYYY-MM'),
               SUM(total_amount)
        FROM orders
        GROUP BY 1
        ORDER BY 1
    """)
    monthly_sales = cur.fetchall()

    cur.close()
    conn.close()

    # ✅ convert to JSON
    product_names = [row[0] for row in top_products]
    product_values = [int(row[1]) for row in top_products]

    return render_template(
        "analysis.html",
        product_names=json.dumps(product_names),
        product_values=json.dumps(product_values),
        top_products=top_products,
        monthly_sales=monthly_sales
    )

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)