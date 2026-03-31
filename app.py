from flask import Flask, render_template, request, redirect, flash
import psycopg2
import json

app = Flask(__name__)
app.secret_key = "replace_with_a_strong_secret"

# DB connection
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="wholesale_erp",
        user="postgres",
        password="5588",
        port="5432"
    )

# ================= DASHBOARD =================
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

    return render_template("dashboard.html",
                           total_products=total_products,
                           total_customers=total_customers,
                           total_orders=total_orders)

# ================= PRODUCTS =================
@app.route("/products", methods=["GET", "POST"])
def products():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        product_name = request.form["name"].strip()
        cur.execute("SELECT 1 FROM products WHERE LOWER(name) = LOWER(%s) LIMIT 1", (product_name,))
        if cur.fetchone():
            flash("Product is already there")
            cur.close()
            conn.close()
            return redirect("/products")

        cur.execute("""
            INSERT INTO products(name, category, price, stock_quantity)
            VALUES (%s,%s,%s,%s)
        """, (
            product_name,
            request.form["category"].strip(),
            request.form["price"],
            request.form["stock"]
        ))
        conn.commit()
        return redirect("/products")

    search = request.args.get("search")

    if search:
        cur.execute("SELECT * FROM products WHERE name ILIKE %s", ('%' + search + '%',))
    else:
        cur.execute("SELECT * FROM products")

    products = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("products.html", products=products)

# ================= CUSTOMERS =================
@app.route("/customers", methods=["GET", "POST"])
def customers():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        customer_name = request.form["name"].strip()
        cur.execute("SELECT 1 FROM customers WHERE LOWER(name) = LOWER(%s) LIMIT 1", (customer_name,))
        if cur.fetchone():
            flash("Customer is already there")
            cur.close()
            conn.close()
            return redirect("/customers")

        cur.execute("""
            INSERT INTO customers(name, contact, address)
            VALUES (%s,%s,%s)
        """, (
            customer_name,
            request.form["contact"].strip(),
            request.form["address"].strip()
        ))
        conn.commit()
        return redirect("/customers")

    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("customers.html", customers=customers)

# ================= ORDERS =================
@app.route("/orders", methods=["GET", "POST"])
def orders():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("CALL create_order(%s,%s,%s)", (
            request.form["customer"],
            request.form["product"],
            request.form["quantity"]
        ))
        conn.commit()
        return redirect("/orders")

    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    cur.execute("SELECT * FROM orders ORDER BY order_id ASC")
    orders = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("orders.html",
                           customers=customers,
                           products=products,
                           orders=orders)

# ================= SUPPLIERS =================
@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        supplier_name = request.form["name"].strip()
        cur.execute("SELECT 1 FROM suppliers WHERE LOWER(name) = LOWER(%s) LIMIT 1", (supplier_name,))
        if cur.fetchone():
            flash("Supplier is already there")
            cur.close()
            conn.close()
            return redirect("/suppliers")

        cur.execute("""
            INSERT INTO suppliers(name, contact, product_supplied)
            VALUES (%s,%s,%s)
        """, (
            supplier_name,
            request.form["contact"].strip(),
            request.form["product"].strip()
        ))
        conn.commit()

    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("suppliers.html", suppliers=suppliers)

# ================= SALES =================
@app.route("/sales")
def sales():

    conn = get_conn()
    cur = conn.cursor()

    # 🔹 Top Selling Products
    cur.execute("""
        SELECT p.name, SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.name
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    top_products = cur.fetchall()

    # 🔹 Monthly Sales
    cur.execute("""
        SELECT TO_CHAR(order_date, 'YYYY-MM') AS month,
               SUM(total_amount)
        FROM orders
        GROUP BY month
        ORDER BY month
    """)
    monthly_sales = cur.fetchall()

    cur.close()
    conn.close()

    # ✅ Convert for chart
    product_names = [row[0] for row in top_products]
    product_values = [int(row[1]) for row in top_products]

    return render_template(
        "analysis.html",
        top_products=top_products,
        monthly_sales=monthly_sales,
        product_names=json.dumps(product_names),
        product_values=json.dumps(product_values)
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)