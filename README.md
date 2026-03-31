# 🧾 Wholesale ERP System

A full-stack Wholesale ERP web application built using **Flask** and **PostgreSQL** to manage inventory, customers, suppliers, orders, and sales insights with a structured relational database.

---

## 📌 Overview

This system is designed to simulate real-world wholesale business operations by handling bulk transactions and maintaining structured data.

It helps in managing:

* Product inventory
* Customer records
* Supplier data
* Order processing
* Sales analytics

---

## 🚀 Features

### Core Features

✔ Product Management (Add, View, Delete)
✔ Customer Management
✔ Supplier Management
✔ Order Creation with Automatic Stock Update
✔ Product Search (ILIKE based search)

### Analytics & Reports

✔ Top-Selling Products Analysis
✔ Monthly Sales Reports
✔ Sales Dashboard with Bar Chart

### System Features

✔ Sidebar Navigation (visible on all pages)
✔ Relational Database Design
✔ Clean Dashboard UI

---

## 🧭 How to Use

| Section   | Description                            |
| --------- | -------------------------------------- |
| Dashboard | View total products, customers, orders |
| Products  | Add, search, delete products           |
| Customers | Manage customer details                |
| Suppliers | Add and manage suppliers               |
| Orders    | Create orders (auto updates stock)     |
| Sales     | View charts and sales reports          |
| Sidebar   | Navigate between modules               |

---

## 🗄️ Database Design

### Tables

* **Products**
* **Customers**
* **Orders**
* **Order_Items**
* **Suppliers**

### Relationships

* One Customer → Many Orders
* One Order → Many Order Items
* One Product → Many Order Items
* Many Products ↔ Many Suppliers

---

## 🧠 SQL Concepts Used

### Functions & Procedures

* Total stock value calculation
* Order processing logic
* Top-selling products retrieval

### Views

* Customer order summary
* Product-wise sales
* Supplier-product mapping

### Queries

* Nested queries (Top customers, low stock, high-value orders)
* Join-based queries (Order details, supplier mapping, monthly sales)

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS, Bootstrap
* **Charts:** Chart.js
* **Tools:** Git, GitHub

---

## 📂 Project Structure

```
wholesale_erp/
│── app.py
│── templates/
│   ├── layout.html
│   ├── dashboard.html
│   ├── products.html
│   ├── customers.html
│   ├── suppliers.html
│   ├── orders.html
│   └── analysis.html
│── requirements.txt
│── README.md
```

Open in browser:
👉 http://127.0.0.1:5000

---

## 👨‍💻 Author

**Surya**
GitHub: https://github.com/Chsurya8

---
