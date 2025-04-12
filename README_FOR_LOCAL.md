
# 🧑‍🏫 FinalProject - Quick Setup Guide for Teachers

This guide helps you run the Django project locally using a provided `.sql` file for the database setup.

---

## 📦 What You Received

- `finalproject.sql` — The complete database dump
- `requirements.txt` — Python dependencies
- `finalproject/` — Django project folder
- `README.md` — This guide

---

## 🛠️ Requirements

Before starting, make sure the following software is installed:

- Python 3.7 or higher
- MySQL Server (e.g., MySQL 8.0)
- pip (Python package manager)
- MySQL client tools (included with MySQL installation)

---

## 🚀 Step-by-Step Setup

### ✅ 1. Create the Database

1. Open **Command Prompt (CMD)**
2. Log in to MySQL:

```bash
mysql -u root -p
```

3. Create the database:

```sql
CREATE DATABASE finalproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

---

### ✅ 2. Import the Provided `.sql` File

Replace `YourName` with your actual Windows username:

```bash
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
mysql -u root -p finalproject < "C:\Users\YourName\Desktop\finalproject.sql"
```

---

### ✅ 3. Install Python Dependencies

1. Open CMD
2. Navigate to the project folder
3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

### ✅ 4. Configure Database Access in Django

Open the file: `finalproject/settings.py` and edit this section to match your MySQL user and password:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finalproject',
        'USER': 'root',  # or your MySQL username
        'PASSWORD': 'yourpassword',  # your MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

---

### ✅ 5. Run the Django Project

```bash
python manage.py runserver
```

Then open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📝 Notes

- If you get an error related to missing packages, try running `pip install -r requirements.txt` again
- If the database is not recognized, double-check the SQL import and MySQL settings

---

## 📬 Need Help?

Contact the project maintainer or refer to the documentation.

Enjoy the project! 🎉
