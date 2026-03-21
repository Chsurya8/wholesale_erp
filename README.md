# 🧾 Wholesale ERP System

A web-based **Wholesale ERP application** built using Flask and PostgreSQL to manage products, customers, and orders efficiently with real-time sales insights.

---

## 📌 Overview

This project helps businesses manage:

* Product inventory
* Customer data
* Order processing
* Sales analysis

It is designed with a **clean dashboard UI** and supports basic ERP operations.

---

## 🚀 Features

✔ Add, view, and delete products
✔ Manage customer details
✔ Create and track orders
✔ Automatic stock updates
✔ Search products by name
✔ Sales analytics (monthly + top products)
✔ Sidebar dashboard UI

---

## 🛠️ Tech Stack

* Backend: Python (Flask)
* Database: PostgreSQL
* Frontend: HTML, CSS, Bootstrap
* Tools: Git, GitHub

---

## 📂 Project Structure

```bash
wholesale_erp/
│── app.py
│── templates/
│   ├── dashboard.html
│   ├── products.html
│   ├── customers.html
│   ├── orders.html
│   └── analysis.html
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/Chsurya8/wholesale_erp.git
cd wholesale_erp
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup Database

Create PostgreSQL database:

```sql
CREATE DATABASE wholesale_erp;
```

Update connection in `app.py`:

```python
conn = psycopg2.connect(
    host="localhost",
    database="wholesale_erp",
    user="postgres",
    password="your_password",
    port="5432"
)
```

---

### 4. Run Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

## 👨‍💻 Author

Surya
GitHub: https://github.com/Chsurya8
