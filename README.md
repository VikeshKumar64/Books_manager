# 📚 Library Management System (Tkinter + MySQL)

A simple desktop **Library Management System** built using **Python (Tkinter)** for the GUI and **MySQL** for data storage.  
This project allows users to manage books, students, and issued books with login authentication.

---

## 🚀 Features

- 🔐 **User Login System**
- 📘 **Add, View, and Delete Books**
- 👨‍🎓 **Add and View Students**
- 🔄 **Issue and Return Books**
- 📅 Tracks issue and return dates automatically
- ✅ Input validation and error handling
- 🎨 Clean and user-friendly Tkinter GUI

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Python (Tkinter) |
| Backend | MySQL |
| Database Connector | `mysql-connector-python` |
| Language | Python 3.x |

---

## 📂 Project Structure

Sql Project/
│
├── data.sql # Database schema and default data
├── db_config.py # Database connection and GUI logic
└── README.md # This file

## ⚙️ Installation & Setup

### 1️⃣ Install Requirements

Make sure you have:

- Python 3.8+  
- MySQL Server (and MySQL Workbench optional)

---

### 2️⃣ Create the Database

Open **MySQL Workbench**, then:

1. Go to **File → Open SQL Script**  
2. Select **`data.sql`**  
3. Click **⚡ Execute**

Confirm your database:

```sql
SHOW DATABASES;
USE vikeshdb;
SHOW TABLES;
```

### 3️⃣ Configure Database Connection
Open db_config.py and update your database credentials:

```
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="vikeshdb"
)
```

### 4️⃣ Run the App
python gui.py

💡 Default Login:

Username: Vikesh
Password: 12345

