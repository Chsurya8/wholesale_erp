# 🧾 Wholesale ERP System

A web-based **Wholesale ERP application** built using Flask and PostgreSQL to manage products, customers, and orders efficiently with real-time sales insights.

---

## 📌 Overview

This project helps businesses manage:

* Product inventory
* Customer data
* Order processing
* Sales analysis

It is designed with a clean dashboard UI and supports basic ERP operations.

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

## 🧭 How to Use

| Section    | What to Do                                   |
| ---------- | -------------------------------------------- |
| Dashboard  | View overall system summary                  |
| Products   | Add, search, and delete products             |
| Customers  | Manage customer details                      |
| Orders     | Create orders and update stock automatically |
| Sales      | Analyze sales performance                    |
| Navigation | Use sidebar to switch between pages          |

---

## 🛠️ Tech Stack

* Backend: Python (Flask)
* Database: PostgreSQL
* Frontend: HTML, CSS, Bootstrap
* Tools: Git, GitHub

---

## 📂 Project Structure

```
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

```
git clone https://github.com/Chsurya8/wholesale_erp.git
cd wholesale_erp
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Setup Database

Create PostgreSQL database:

```
CREATE DATABASE wholesale_erp;
```

Update connection in `app.py`.

---

### 4. Run Application

```
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 👨‍💻 Author

Surya
GitHub: https://github.com/Chsurya8
